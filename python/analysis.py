#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[64]:


import geopandas as gpd
from shapely.wkt import loads
import pandas as pd
from shapely.geometry import Point, MultiPolygon


# # Read Data

# In[65]:


outlines = gpd.read_file('../data/employment_center_outlines.csv').drop(columns=['geometry'])
outlines['the_geom'] = outlines['the_geom'].apply(loads)
outlines = outlines.set_geometry('the_geom')


# In[66]:


tracts = gpd.read_file('../data/tracts.csv').drop(columns=['geometry'])
tracts['the_geom'] = tracts['the_geom'].apply(loads)
tracts = tracts.set_geometry('the_geom')


# In[67]:


income = gpd.read_file('../data/income_estimates.csv').drop(columns=['geometry'])


# # Merge Tracts and Outlines on Centroids

# In[68]:


def get_centroid(df):
    polygons = df['the_geom']
    if isinstance(polygons, MultiPolygon) or isinstance(polygons, Polygon):
        return polygons.centroid
    else:
        return None


# In[69]:


outlines['centroid'] = outlines.apply(get_centroid, axis=1)
tracts['centroid'] = tracts.apply(get_centroid, axis=1)
outlines_and_tracts = outlines.sjoin_nearest(tracts, how='left', distance_col='centroid')


# # Merge Tracts and Outlines on Income

# In[70]:


income['households']=income['households'].astype(int)
maxes = income[income['yr_id']=='2022'].groupby(['tract']).max()[['households']].reset_index()
maxes['tract'] = maxes['tract'].astype(str)
merged_not_equal = income.merge(maxes,how='right',on='tract', suffixes=('_right', '_left'))
merge_income= merged_not_equal[merged_not_equal['households_right']==merged_not_equal['households_left']][merged_not_equal['yr_id']=='2022'][merged_not_equal['households_left'].astype(int)>0]


# In[71]:


spatial_income = outlines_and_tracts.merge(merge_income, left_on='CT2010DT', right_on='tract',how='left')


# In[72]:


#EPSG 2230 _> centroid to centroid 
spatial_income.explore()


# In[73]:


income[income['tract']=='201.05']


# In[74]:


df = pd.read_csv("../data/wac_data/ca_wac_S000_JT00_2021.csv.gz", compression='gzip', dtype={'w_geocode': 'str'})
df


# In[75]:


sd_county = df[df['w_geocode'].str[:5] == '06073']


# In[76]:


sd_county['tract'] = sd_county['w_geocode'].str[5:11]


# In[77]:


sd_county.groupby(['tract']).sum()


# In[78]:


sd_county[sd_county['w_geocode'].str[-4:] == '1000']


# In[79]:


blocks = pd.read_csv("../data/Census_Blocks_2020_20231117.csv", dtype={'GEOID20': 'str'})
blocks.head()


# In[80]:


blocks[blocks['BLOCK'] == 1000]


# In[81]:


blocks.join(sd_county, lsuffix='GEOID20', rsuffix='w_geocode').info()


# In[82]:


sd_county.join(blocks, lsuffix='w_geocode', rsuffix='GEOID20')


# In[83]:


# Smaller blocks (find centroid), spatial join on employment center
blocks.head()


# In[84]:


blocks['GEOID20'].str.len()


# In[85]:


sd_county['w_geocode'].str.len()


# In[86]:


blocks[blocks["GEOID20"] == "060730001001000"]


# In[87]:


# Get all segments of workforce data, loop through each one filter for SD county, then create one big data frame, join the data with census blocks -> check if centroids exist
# in employment center of Downtown
directory = '../data/wac_data'
import os


# In[88]:


os.listdir(directory)


# In[89]:


complete_df = pd.DataFrame()
for file in os.listdir(directory):
    if file.split(".")[-1] == 'gz':
        #add to df
        df = pd.read_csv(os.path.join(directory, file), compression='gzip', dtype={'w_geocode': 'str'})
        complete_df = pd.concat([complete_df, df], ignore_index=True)

complete_df


# In[90]:


san_diego = complete_df[complete_df['w_geocode'].str[:5] == '06073']
san_diego


# In[91]:


merged_data = san_diego.merge(blocks, left_on="w_geocode", right_on="GEOID20")


# In[92]:


merged_data.columns


# In[93]:


merged_data.groupby("w_geocode").sum()


# In[94]:


merged_data['the_geom'] = merged_data['the_geom'].apply(loads)
merged_data = merged_data.set_geometry('the_geom')


# In[95]:


merged_data = merged_data.set_geometry('the_geom')


# In[96]:


merged_data['centroid'] = merged_data.apply(get_centroid, axis=1)


# In[97]:


merged_data


# In[98]:


outlines = gpd.read_file('../data/employment_center_outlines.csv').drop(columns=['geometry'])
outlines['the_geom'] = outlines['the_geom'].apply(loads)
outlines = outlines.set_geometry('the_geom')


# In[99]:


outlines["centroid"] = outlines[outlines['Name'] == 'Downtown'].apply(get_centroid, axis=1)
dt_point = outlines[outlines["Name"] == "Downtown"]
dt_point


# In[100]:


outlines_and_tracts = dt_point.sjoin_nearest(merged_data, how='left', distance_col='centroid')

outlines_and_tracts.to_csv('../output/dt_data.csv', index=False)


# In[101]:


# multipolygon = MultiPolygon([loads(downtown_df['the_geom'].iloc[0])])

# # Create a Point object for each centroid
# merged_data['point'] = merged_data['centroid'].apply(lambda x: loads(x))

# # Check if each centroid is within the Multipolygon
# merged_data['within_polygon'] = merged_data['point'].apply(lambda point: point.within(multipolygon))

# # Filter the centroids that are within the Multipolygon
# filtered_centroids_df = merged_data[merged_data['within_polygon']]

# # Drop unnecessary columns
# filtered_centroids_df = filtered_centroids_df.drop(columns=['point', 'within_polygon'])

# # filtered_centroids_df
# from shapely.wkt import loads

# # Assuming you have a DataFrame with a column 'the_geom' containing the MULTIPOLYGON
# multipolygon_wkt = downtown_df['the_geom'].iloc[0]
# multipolygon = loads(multipolygon_wkt)

# # Create a Point object for each centroid
# merged_data['point'] = merged_data['centroid'].apply(lambda x: loads(x))

# # Check if each centroid is within the Multipolygon
# merged_data['within_polygon'] = merged_data['point'].apply(lambda point: point.within(multipolygon))

# # Filter the centroids that are within the Multipolygon
# filtered_centroids_df = merged_data[merged_data['within_polygon']]

# # Drop unnecessary columns
# filtered_centroids_df = filtered_centroids_df.drop(columns=['point', 'within_polygon'])

# filtered_centroids_df


# In[ ]:




