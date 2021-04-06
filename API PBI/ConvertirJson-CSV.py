#!/usr/bin/env python
# coding: utf-8

# In[38]:


#!pip install pandas
#!pip install xlsxwriter
#!pip install xlrd
#!pip install openpyxl


# In[2]:


import json 
import pandas as pd


# In[3]:


pathReportHistorico = ".\Json Origen\ReportHistorico.json"
pathDashboardHistorico = ".\Json Origen\DashboardHistorico.json"


# In[4]:


df_josn = pd.read_json(pathReportHistorico)
df_josn.to_excel('ReportHistorico.xlsx', index=False)
df_josn = pd.read_json(pathReportHistorico)
df_josn.to_excel('DashboardHistorico.xlsx', index=False)


# In[ ]:




