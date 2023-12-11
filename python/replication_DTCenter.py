#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


downtown = pd.read_csv('../data/dt_data.csv')


# In[6]:


region = pd.read_csv('../data/region_data.csv')


# Table 1
# CNS 1 - 20

# In[7]:


job_categories = ['Agriculture, Forestry, Fishing and Hunting',
                 'Mining, Quarrying, and Oil and Gas Extraction',
                 'Utilities','Construction','Manufacturing','Wholesale Trade',
                  'Retail Trade','Transportation and Warehousing','Information',
                  'Finance and Insurance','Real Estate and Rental and Leasing',
                  'Professional, Scientific, and Technical Services','Management of Companies and Enterprises',
                  'Administrative and Support and Waste Management and Remediation Services',
                  'Educational Services','Health Care and Social Assistance','Arts, Entertainment, and Recreation',
                  'Accommodation and Food Services','Other Services except Public Administration',
                  'Public Administration']


# In[8]:


len(job_categories)


# Downtown Querying

# In[9]:


# Create an empty dictionary to store the sums
dt_sums = {}

# Loop through the column names from "CNS01" to "CNS20"
for column_name in [f'CNS{i:02d}' for i in range(1, 21)]:
    column_sum = downtown[column_name].sum()
    dt_sums[column_name] = column_sum

# Now, column_sums is a dictionary where keys are column names like "CNS01", "CNS02", ..., "CNS20",
# and values are the sums of the respective columns
print(dt_sums)


# In[10]:


dt_df = pd.DataFrame.from_dict(dt_sums, orient='index', columns=['Sum'])
dt_df.index = job_categories
dt_df = dt_df.rename(columns={"Sum": "Total jobs"})


# In[11]:


total_jobs_dt = dt_df['Total jobs'].sum()
total_jobs_dt


# Regional Querying

# In[12]:


# Create an empty dictionary to store the sums
regional_sums = {}

# Loop through the column names from "CNS01" to "CNS20"
for column_name in [f'CNS{i:02d}' for i in range(1, 21)]:
    column_sum = region[column_name].sum()
    regional_sums[column_name] = column_sum

# Now, column_sums is a dictionary where keys are column names like "CNS01", "CNS02", ..., "CNS20",
# and values are the sums of the respective columns
print(regional_sums)


# In[13]:


region_df = pd.DataFrame.from_dict(regional_sums, orient='index', columns=['Sum'])
region_df.index = job_categories
region_df = region_df.rename(columns={"Sum": "Total jobs"})


# In[14]:


total_jobs_region = region_df['Total jobs'].sum()
total_jobs_region


# Table 1 Code

# In[15]:


dt_df['% of jobs'] = (dt_df['Total jobs'] / total_jobs_dt * 100)
dt_df = dt_df.sort_values(by='% of jobs',ascending = False)
dt_df['% of jobs'] = dt_df['% of jobs'].apply(lambda x: f'{x:.2f}%')


# # Who works and lives in the Downtown San Diego employment center?

# ## Highlight Table 1
# Of the 293,292 jobs in
# the Downtown San Diego
# employment center, the top
# five are categorized as Public Administration, Professional, Scientific, and Technical Services,
# Accommodation and Food Services	, Transportation and Warehousing, and health care and
# Social assistance. Compared
# to the region overall, there
# is an overrepresentation of
# accommodations and
# local government and an
# underrepresentation of retail.

# In[16]:


dt_df.head(10)


# In[17]:


dt_df.to_csv('output/DowntownJobDistribution.csv')


# ## Figure 1

# In[18]:


college_degree_jobs_dt = downtown['CD04'].sum()
college_degree_jobs_region = region['CD04'].sum()


# In[19]:


percentage_college_dt = (college_degree_jobs_dt / total_jobs_dt) * 100
percentage_college_region = (college_degree_jobs_region / total_jobs_region) * 100
formatted_percentage_dt = f"{percentage_college_dt:.2f}%"
formatted_percentage_region = f"{percentage_college_region:.2f}%"


# In[20]:


'Downtown College Degree Percent: ' + formatted_percentage_dt


# In[21]:


'Region College Degree Percent: ' + formatted_percentage_region


# ## Around 27% of workers in the downtown employment center have a 4-year college degree (or higher), a little higher than the regional average (24%).
