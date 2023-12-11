#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
from shapely.wkt import loads
import pandas as pd
from shapely.geometry import Point, MultiPolygon

pd.options.display.float_format = '{:.0f}'.format


# In[2]:


# Read in downtown data and get geocodes
dt_data = pd.read_csv('../output/dt_data.csv', dtype={'w_geocode': 'str'})
dt_geocodes = dt_data['w_geocode'].unique()


# In[3]:


# Get all origin-destination data for California
main_data = pd.read_csv('../data/ca_od_main_JT00_2021.csv.gz', dtype={'w_geocode': 'str', 'h_geocode': 'int'}, compression='gzip')
main_data


# In[4]:


# Filter for only Downtown SD as the workplace location
downtown_od = main_data[main_data['w_geocode'].isin(dt_geocodes)]


# In[5]:


# Fix the origin geocode (was missing an initial front 0)
downtown_od['h_geocode'] = '0' + downtown_od['h_geocode'].astype('str')


# In[6]:


census_blocks = gpd.read_file('../data/Census_Blocks_20231127.csv', dtype={'GEOID20': 'str'}).drop(columns=['geometry'])
census_blocks['the_geom'] = census_blocks['the_geom'].apply(loads)
census_blocks = census_blocks.set_geometry('the_geom')


# In[7]:


merged_data = downtown_od.merge(census_blocks, left_on="h_geocode", right_on="GEOID20")


# In[8]:


def get_centroid(df):
    polygons = df['the_geom']
    if isinstance(polygons, MultiPolygon) or isinstance(polygons, Polygon):
        return polygons.centroid
    else:
        return None


# In[9]:


merged_data.info()


# In[10]:


merged_data.head()


# In[11]:


merged_data['centroid'] = merged_data.apply(get_centroid, axis=1)
merged_data


# In[12]:


outlines = gpd.read_file('../data/Jurisdictions.csv').drop(columns=['geometry'])
outlines['the_geom'] = outlines['the_geom'].apply(loads)
outlines = outlines.set_geometry('the_geom')


# In[13]:


outlines.info()


# In[14]:


outlines


# In[15]:


ec_dict = outlines[['the_geom', 'NAME']]


# In[16]:


employment_center = [0] * merged_data.shape[0]

for row in merged_data.iterrows():
    row_centroid = row[1]['centroid']
    for juris in ec_dict.iterrows():
        if row_centroid.within(juris[1]['the_geom']):
            employment_center[row[0]] = juris[1]['NAME']

employment_center
#merged_data['within_polygon'] = merged_data['centroid'].apply(lambda point: point.within())


# In[17]:


len(employment_center)


# In[18]:


merged_data.shape[0]


# In[19]:


merged_data['Employment Center'] = list(map(lambda x: 'N/A' if x == 0 else x, employment_center))


# In[20]:


pd.set_option("display.max_rows", 0)

origin_destination_final = merged_data['Employment Center'].value_counts()


# In[21]:


od_final = origin_destination_final.to_frame().reset_index()
od_final['Total %'] = (od_final['count'] / od_final['count'].sum() * 100).apply(lambda x: f'{x:.2f}%')


# In[30]:


map_jurisdiction = od_final.merge(outlines, left_on='Employment Center', right_on='NAME', how='left')[['Employment Center', 'count', 'Total %', 'the_geom']]


# In[31]:


map_jurisdiction.to_csv('../output/map_jurisdiction.csv')


# In[112]:


# Page 6


# In[ ]:




