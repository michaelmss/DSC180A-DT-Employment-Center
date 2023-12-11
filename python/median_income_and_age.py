#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[95]:


import geopandas as gpd
from shapely.wkt import loads
import pandas as pd
from shapely.geometry import Point, MultiPolygon


# # Read Data

# In[96]:


outlines = gpd.read_file('data/employment_center_outlines.csv').drop(columns=['geometry'])
outlines['the_geom'] = outlines['the_geom'].apply(loads)
outlines = outlines.set_geometry('the_geom')


# In[97]:


tracts = gpd.read_file('data/tracts.csv').drop(columns=['geometry'])
tracts['the_geom'] = tracts['the_geom'].apply(loads)
tracts = tracts.set_geometry('the_geom')


# In[98]:


income = gpd.read_file('data/income_estimates.csv').drop(columns=['geometry'])


# # Merge Tracts and Outlines on Centroids

# In[99]:


def get_centroid(df):
    polygons = df['the_geom']
    if isinstance(polygons, MultiPolygon) or isinstance(polygons, Polygon):
        return polygons.centroid
    else:
        return None


# In[100]:


outlines['centroid'] = outlines.apply(get_centroid, axis=1)
tracts['centroid'] = tracts.apply(get_centroid, axis=1)
outlines_and_tracts = outlines.sjoin_nearest(tracts, how='left', distance_col='centroid')


# # Merge Tracts and Outlines on Income

# In[101]:


income['households']=income['households'].astype(int)
maxes = income[income['yr_id']=='2022'].groupby(['tract']).max()[['households']].reset_index()
maxes['tract'] = maxes['tract'].astype(str)
merged_not_equal = income.merge(maxes,how='right',on='tract', suffixes=('_right', '_left'))
merge_income= merged_not_equal[merged_not_equal['households_right']==merged_not_equal['households_left']][merged_not_equal['yr_id']=='2022'][merged_not_equal['households_left'].astype(int)>0]


# In[102]:


spatial_income = outlines_and_tracts.merge(merge_income, left_on='CT2010DT', right_on='tract',how='left')


# # Finding Median Income

# In[103]:


# Define a function to calculate the median of the income range
def calculate_median_income(income_range):
    if 'or more' in income_range:
        # Take the lower bound for 'or more'
        lower_bound = int(income_range.replace('$', '').replace('or more', '').replace(',', '').strip())
        return lower_bound
    elif 'Less than' in income_range:
        # Take the upper bound for 'Less than'
        upper_bound = int(income_range.replace('Less than $', '').replace(',', '').strip())
        return upper_bound
    else:
        # Split the range and calculate the median
        lower_bound, upper_bound = [int(s.replace('$', '').replace(',', '').strip()) for s in income_range.split('to')]
        return (lower_bound + upper_bound) // 2


# # Median Income by Households

# Separating Downtown Data by Tract and Most Recent Year

# In[104]:


incomes_dt = income[income['tract']=='201.05']


# In[105]:


median_income_2022_dt = incomes_dt[incomes_dt['yr_id'] == '2022']


# In[106]:


median_income_2022_dt


# In[107]:


median_income_2022_dt['income'] = median_income_2022_dt['name'].apply(calculate_median_income)


# In[108]:


median_income_2022_dt


# In[109]:


# Assume median_income_2022_dt is your DataFrame with 'households' and 'income' columns
median_income_2022_dt['cumulative_frequency'] = median_income_2022_dt['households'].cumsum()
total_households = median_income_2022_dt['households'].sum()
median_position = total_households / 2
median_class_interval = median_income_2022_dt[median_income_2022_dt['cumulative_frequency'] >= median_position].iloc[0]

# Calculate the lower boundary of the median class interval
L = (median_class_interval['income'] - 
     (median_class_interval['income'] - 
      median_income_2022_dt[median_income_2022_dt['income'] < median_class_interval['income']]['income'].max()) / 2)

# If the median class is the first class, L would be 0 (or another reasonable assumption)
F = median_income_2022_dt[median_income_2022_dt['income'] < median_class_interval['income']]['households'].sum()
f = median_class_interval['households']
W = (median_income_2022_dt['income'].iloc[1] - median_income_2022_dt['income'].iloc[0])
median_income_dt = L + ((median_position - F) / f) * W
median_income_dt = round(median_income_dt)


# # Median Household Income for Downtown Employment Center

# In[110]:


median_income_dt


# # Median Income by Household Region

# In[111]:


incomes_region = pd.read_csv('data/2022_Estimates_Household_Income_by_2020_Census_Tract.csv')


# In[112]:


incomes_region[incomes_region['yr_id'] == 2022]


# In[113]:


median_income_2022_region = incomes_region.groupby('name').sum().reset_index()
median_income_2022_region = median_income_2022_region[['name', 'households']]
median_income_2022_region


# In[114]:


median_income_2022_region['income'] = median_income_2022_region['name'].apply(calculate_median_income)


# In[115]:


median_income_2022_region = median_income_2022_region.sort_values(by='income')


# In[116]:


median_income_2022_region


# In[117]:


# Assume median_income_2022_dt is your DataFrame with 'households' and 'income' columns
median_income_2022_region['cumulative_frequency'] = median_income_2022_region['households'].cumsum()
total_households = median_income_2022_region['households'].sum()
median_position = total_households / 2
median_class_interval = median_income_2022_region[median_income_2022_region['cumulative_frequency'] >= median_position].iloc[0]

# Calculate the lower boundary of the median class interval
L = (median_class_interval['income'] - 
     (median_class_interval['income'] - 
      median_income_2022_region[median_income_2022_region['income'] < median_class_interval['income']]['income'].max()) / 2)

# If the median class is the first class, L would be 0 (or another reasonable assumption)
F = median_income_2022_region[median_income_2022_region['income'] < median_class_interval['income']]['households'].sum()
f = median_class_interval['households']
W = (median_income_2022_region['income'].iloc[1] - median_income_2022_region['income'].iloc[0])
median_income_region = L + ((median_position - F) / f) * W
median_income_region = round(median_income_region)


# # Median Household Income for Region

# In[118]:


median_income_region


# # Median Ages

# In[119]:


#function to handle all cases including 'Under 5' and '85 and Older'
def calculate_median_age(age_range):
    # Handle the 'Under 5' case
    if age_range == 'Under 5':
        return 5  # Assuming median age between 0 and 5 is 2.5
    # Handle the '85 and Older' case
    elif age_range == '85 and Older':
        return 85  # Assuming 85 as the median age for '85 and Older'
    # Handle the 'and' in age range
    elif 'and' in age_range:
        # Take the average of the two numbers
        ages = age_range.replace('and', '').split()
        return sum(map(int, ages)) / 2
    # Handle the 'to' in age range
    else:
        ages = age_range.split(' to ')
        return (int(ages[0]) + int(ages[1])) / 2


# In[120]:


import numpy as np


# In[121]:


ages_region = pd.read_csv('data/2022_Estimates_Population_by_Age_by_2020_Census_Tract.csv')


# # Median Age DT Employment Center

# In[122]:


ages_dt = ages_region[ages_region['tract'] == 201.05]
ages_dt_2022 = ages_dt[ages_dt['yr_id'] == 2022]


# In[123]:


ages_dt_2022.head()


# In[124]:


# Apply the revised function to the 'name' column to create 'weighted age'
ages_dt_2022['weighted age'] = ages_dt_2022['name'].apply(calculate_median_age)
ages_dt_2022.head()


# In[125]:


# Assume ages_dt_2022 is your DataFrame with 'population' and 'weighted_age' columns
ages_dt_2022['cumulative_population'] = ages_dt_2022['population'].cumsum()
total_population = ages_dt_2022['population'].sum()
median_position = total_population / 2
median_age_group = ages_dt_2022[ages_dt_2022['cumulative_population'] >= median_position].iloc[0]

# Calculate the lower boundary of the median age group
L = ages_dt_2022[ages_dt_2022['weighted age'] < median_age_group['weighted age']]['weighted age'].max()
# If the median age group is the first group, L would be 0 (or another reasonable assumption)
F = ages_dt_2022[ages_dt_2022['weighted age'] < median_age_group['weighted age']]['population'].sum()
f = median_age_group['population']
W = median_age_group['weighted age'] - L if L != 0 else median_age_group['weighted age'] - ages_dt_2022.iloc[0]['weighted age']
median_age_dt = L + ((median_position - F) / f) * W
median_age_dt = round(median_age_dt,2)


# # Median Age of Downtown Employment Center

# In[126]:


median_age_dt


# # Median Age for Region

# In[127]:


ages_region_2022 = ages_region[ages_region['yr_id'] == 2022]


# In[128]:


ages_region_2022['weighted age'] = ages_region_2022['name'].apply(calculate_median_age)
ages_region_2022 = ages_region_2022.groupby('weighted age').sum().reset_index()


# In[129]:


ages_region_2022.head()


# In[130]:


# Assume ages_dt_2022 is your DataFrame with 'population' and 'weighted_age' columns
ages_region_2022['cumulative_population'] = ages_region_2022['population'].cumsum()
total_population = ages_region_2022['population'].sum()
median_position = total_population / 2
median_age_group = ages_region_2022[ages_region_2022['cumulative_population'] >= median_position].iloc[0]

# Calculate the lower boundary of the median age group
L = ages_region_2022[ages_region_2022['weighted age'] < median_age_group['weighted age']]['weighted age'].max()
# If the median age group is the first group, L would be 0 (or another reasonable assumption)
F = ages_region_2022[ages_region_2022['weighted age'] < median_age_group['weighted age']]['population'].sum()
f = median_age_group['population']
W = median_age_group['weighted age'] - L if L != 0 else median_age_group['weighted age'] - ages_region_2022.iloc[0]['weighted age']
median_age_region = L + ((median_position - F) / f) * W
median_age_region = round(median_age_region,2)


# # Median Age of Region

# In[131]:


median_age_region


# # Converting Median Incomes and Age to Dataframe

# In[135]:


median_values = {'MedianIncomeDT': median_income_dt,
                 'MedianIncomeRegion': median_income_region,
                 'MedianAgeDT': median_age_dt,
                 'MedianAgeRegion': median_age_region}
# If you want Pandas to generate an index automatically
final_df = pd.DataFrame(data=median_values,index = [0])


# Commented out for not using

# In[138]:


# final_df.to_csv('output/ages_and_income.csv')


# In[139]:


final_df


# In[ ]:




