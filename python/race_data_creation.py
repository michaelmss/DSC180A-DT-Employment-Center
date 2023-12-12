#!/usr/bin/env python
# coding: utf-8

# In[30]:


import warnings
warnings.filterwarnings("ignore")
import pandas as pd


# In[31]:


df = pd.read_csv("../output/dt_data.csv")


# In[32]:


df = df.rename(columns={'CR01': 'White', 'CR02': 'Black', "CR03": "Native American", "CR04": "Asian", "CR05": "Hawaiian" , "CR07": "Two or more", "CT02": "Hispanic"})
# df.head()


# In[33]:


df.columns


# In[43]:


dt_race = df[["White", "Black", "Native American", "Asian", "Hawaiian", "Hispanic","Two or more"]].sum().to_frame()#.to_csv("race_dt.csv")


# In[41]:


df


# In[35]:


df2 = pd.read_csv("../output/region_data.csv")


# In[37]:


df2 = df2.rename(columns={'CR01': 'White', 'CR02': 'Black', "CR03": "Native American", "CR04": "Asian", "CR05": "Hawaiian" , "CR07": "Two or more", "CT02": "Hispanic"})
#df2.head()


# In[44]:


region_race = df2[["White", "Black", "Native American", "Asian", "Hawaiian", "Hispanic","Two or more"]].sum().to_frame()#.to_csv("race_region.csv")


# In[48]:


out = pd.merge(region_race, dt_race, left_index=True, right_index=True)#.to_csv("race_region.csv")


# In[51]:


out.to_csv("../output/race_all.csv")


# In[64]:


out = out.T.reset_index(drop=True)


# In[68]:


region = ["Region", "Downtown"]


# In[71]:


out["Location"] = region


# In[73]:


out.to_csv("../output/race_all.csv")


# In[ ]:




