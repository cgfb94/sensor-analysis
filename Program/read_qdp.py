#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re 


# In[2]:


def read_qdp(file_name, make_excel = False, x = 'bias', y = 'V fb (V)'):
    '''
    Accepts a raw sting literal for the filename and path.
    x and y are strings which name the first 2 columns, default to bias
    and V fb (V)
    If make_excel is set to True then excel file is created in the name
    of the input file.
    Return the a pandas dataframe with the data. 
    '''
    #name first two cols after inputs
    cols = {0: x, 1: y}
    header = 0
    #precompile the regexes for use in loop
    col_nam_re = re.compile(r'la\sy(\d)\s(.+)')
    data_match_re = re.compile(r'^-?(\d.+)')
    
    with open(file_name) as file:
        for line in file:
            column_match = col_nam_re.match(line)
            if column_match:
                #remove any formatting from col names
                cols[int(column_match.group(1))] = re.sub(r'(\\d|\\u)',r' ', column_match.group(2))
            else:
                #once data is matched, loop break and record header
                data_match = data_match_re.match(line)
                if data_match:
                    break
            header += 1
    #reads table with whitespace seperators (tab or space)
    
    
    df = pd.read_csv(file_name, sep='\s+', header=None, skiprows=header, index_col=False, comment='!')
    
 
    #make list of col names for df and number ones without labels
    col_names = []
    for i in range(len(df.columns)):
        try:
             col_names.append(cols[i])
        except:
            col_names.append(str(i))
        i += 1
            
    #set column names and sort by x vals    
    df.columns = col_names
    df.sort_values(by=[x], inplace=True)
    
    if df.iloc[:,0][1] * df.iloc[:,1][1] < 0:
        df.iloc[:,1] *= -1
    
    if make_excel:
        #find name for excel sheet from end of path
        name_match = re.search(r'(\\?((?:.(?!\\))+)$)', file_name)
        name = re.sub(r'(\.qdp|\\)', r'', name_match.group(1))
        #write to file and save
        writer = pd.ExcelWriter(str(name)+'.xlsx')
        df.to_excel(writer,'Sheet1',index=False)
        writer.save()
        
    return df

