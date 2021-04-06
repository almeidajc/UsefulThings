#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json 
import pandas as pd


# In[66]:


pathReportHistorico = ".\Json Origen\ReportHistorico2.json"
pathDashboardHistorico = ".\Json Origen\DashboardHistorico.json"


# In[67]:


df_josnHistorico = pd.read_json(pathReportHistorico)


# In[68]:


pathReportesWorkspace = ".\Json Origen\ReportesWorkspace.json"
df_josnReportesWorkspace = pd.read_json(pathReportesWorkspace)


# In[ ]:


df_josnReportesWorkspace.merge(df_josnHistorico[df_josnHistorico.UserId = 'LescanoS@sancristobal.com.ar'], left_on='ReportId', right_on='ReportId', how='inner')


# In[ ]:


df_josnHistorico
df_josnReportesWorkspace


# In[57]:


df_josnHistorico[df_josnHistorico.UserId == 'LescanoS@sancristobal.com.ar']


# In[105]:


dfmerge = df_josnReportesWorkspace.merge(df_josnHistorico[df_josnHistorico.UserId == 'LescanoS@sancristobal.com.ar'], left_on='id', right_on='ReportId', how='right')
dfmerge


# In[106]:


dfmerge = dfmerge.rename(columns={'name_x':'name','name_y':'NombreReportes'})
#dfmerge = dfmerge.drop(['ClientIP','IsSuccess','UserAgent'],inplace=True, axis=1)
dfmerge.drop(['ClientIP','IsSuccess','UserAgent'],inplace=True, axis=1)


# In[107]:


dfmerge


# In[108]:


dfmerge.to_excel('TestJoin.xlsx', index=False)


# In[ ]:




