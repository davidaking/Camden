# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:13:07 2020

@author: david
"""

import os

file_path = os.path.dirname(os.path.realpath(__file__))
file_path = [file_path][0]
os.chdir(file_path)


path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)


for sub_dir_name in os.listdir():
    if os.path.isdir(sub_dir_name) and sub_dir_name != '.git':
        str_1 = f'{sub_dir_name}_dir = '
        str_2 = f'"{path_parent}/{sub_dir_name}/"'
        str_2 = str_2.replace('\\','/')
        my_code = str_1 + str_2
        exec(my_code,globals())

    

