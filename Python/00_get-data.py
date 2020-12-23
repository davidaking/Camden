
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 19:01:37 2020

Script to access and merge Camden postcode, IMD and population data

Run 00_get-path.py first to set up directory variables



References:

Postcode data:
     
https://opendata.camden.gov.uk    
    
IMD data:   

https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019
    
Population data:
https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/lowersuperoutputareamidyearpopulationestimates
https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/lowersuperoutputareamidyearpopulationestimates
https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/lowersuperoutputareamidyearpopulationestimatesnationalstatistics
    
    
@author: david
"""

import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json as JSON
import os
import zipfile

# Import postcode data
url = 'https://opendata.camden.gov.uk/resource/gkhg-q337.json'
json_data = requests.get(url).json()

# First element of list
test_data = json_data[0]


# Column names from keys of test_data
col_names = list(test_data.keys())

# Set up empty dataframe to hold data
df_pc = pd.DataFrame(columns=col_names,index=range(len(json_data)))
#df_pc.shape
# Loop through post code data populating dataframe
for i in range(len(json_data)):
    lst_el = json_data[i]
    df_pc.iloc[i,:] = list(lst_el.values())



# Bring in indices of multiple deprivation
search_file = r'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/833970/File_1_-_IMD2019_Index_of_Multiple_Deprivation.xlsx'
xl = pd.ExcelFile(search_file)

#xl.sheet_names
df_IMD = xl.parse('IMD2019')

# Extract indices corresponding to Camden LSOA column
df_IMD_Cam = pd.DataFrame(index=df_pc.index,columns=df_IMD.columns)

lsoa_code = df_pc['lsoa_code']

for i in range(len(lsoa_code)):

    ind = df_IMD['LSOA code (2011)'] == lsoa_code[i]
    df_IMD_Cam.iloc[i,:]= df_IMD[ind].values
    
    
    
# Merge dataframes    
df_pc = pd.merge(df_pc,df_IMD_Cam,left_index=True,right_index=True)


#df_pc.head(1).T
#df_pc.tail(1).T


# Population data
  
#os.listdir(data_dir)

# Unzip population data
file_zip = f'{data_dir}sape22dt2mid2019lsoasyoaestimatesunformatted.zip' 

with zipfile.ZipFile(file_zip,"r") as zip_ref:
    zip_ref.extractall(data_dir)    


#os.listdir(data_dir)

# Read in unzipped Excel file
search_file = f'{data_dir}SAPE22DT2-mid-2019-lsoa-syoa-estimates-unformatted.xlsx'
xl = pd.ExcelFile(search_file)

# Extract 2019 population data
df_pop = xl.parse('Mid-2019 Persons',skiprows=4)


# Extract population data for Camden
df_pop_Cam = pd.DataFrame(index=df_pc.index,columns=df_pop.columns)

lsoa_code = df_pc['lsoa_code']

for i in range(len(lsoa_code)):

    ind = df_pop['LSOA Code'] == lsoa_code[i]
    df_pop_Cam.iloc[i,:]= df_pop[ind].values
    
   
# Merge with post code and IMD data   
df_pc = pd.merge(df_pc,df_pop_Cam,left_index=True,right_index=True)


# Add latitude and longitude to df_pc
df_pc['latitude'] = [df_pc.loc[i,'location']['latitude'] for i in df_pc.index]
df_pc['longitude'] = [df_pc.loc[i,'location']['longitude'] for i in df_pc.index]


# Remove 'location' column

df_pc.pop('location')


# Export data to SQLite
export_file = f'sqlite:///{data_dir}Camden-data.db'
engine = create_engine(export_file, echo=False)
conn =  engine.connect()
df_pc.to_sql('Camden_data', conn,if_exists='replace')

# Close connection
conn.close()


