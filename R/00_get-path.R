

# Script to define variables for directory names

path <- dirname(rstudioapi::getActiveDocumentContext()$path)
path <- dirname(path)


dir_list <- list.dirs(path,recursive = FALSE)
dir_list <- gsub(paste0(path,"/"), "", dir_list)


for (sub_dir_name in dir_list){
  
  if (sub_dir_name != ".git"){
    
    
    str_1 = paste0(sub_dir_name,"_dir <- ")
    str_2 = paste0("'",path,"/",sub_dir_name,"/'")
    my_code <- paste0(str_1,str_2)
    eval(parse(text=my_code))
    
    
  }
  
  
  
}


