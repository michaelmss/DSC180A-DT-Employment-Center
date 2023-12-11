#!/usr/bin/env python
# coding: utf-8

# In[2]:


import geopandas as gpd
from shapely.wkt import loads
import pandas as pd
from shapely.geometry import MultiPolygon


# In[72]:


lehd_od = pd.read_csv('../data/ca_od_main_JT00_2021.csv.gz', compression='gzip')


# In[73]:



lehd_od['w_geocode'] = lehd_od['w_geocode'].astype(str)
lehd_od['h_geocode'] = lehd_od['h_geocode'].astype(str)

lehd_od['w_block'] = lehd_od['w_geocode'].str.strip().str[-4:]
lehd_od['h_block'] = lehd_od['h_geocode'].str.strip().str[-4:]


# In[74]:


# filter by san diego as well
lehd_od['w_tract'] = lehd_od['w_geocode'].str.strip().str[-10:-4]
lehd_od['w_state_county'] = lehd_od['w_geocode'].str.strip().str[-15:-10]
lehd_od['h_tract'] = lehd_od['h_geocode'].str.strip().str[-10:-4]


# In[75]:


only_downtown = lehd_od[(lehd_od['w_tract']=='006200')]


# In[77]:


only_downtown.groupby('h_geocode').count()


# In[ ]:





# In[20]:


# outlines = gpd.read_file('../data/employment_center_outlines.csv').drop(columns=['geometry'])
# outlines['the_geom'] = outlines['the_geom'].apply(loads)
# outlines = outlines.set_geometry('the_geom')
# tracts = gpd.read_file('../data/tracts.csv').drop(columns=['geometry'])
# tracts['the_geom'] = tracts['the_geom'].apply(loads)
# tracts = tracts.set_geometry('the_geom')
# def get_centroid(df):
#     polygons = df['the_geom']
#     if isinstance(polygons, MultiPolygon) or isinstance(polygons, Polygon):
#         return polygons.centroid
#     else:
#         return None
# outlines['centroid'] = outlines.apply(get_centroid, axis=1)
# tracts['centroid'] = tracts.apply(get_centroid, axis=1)
# outlines_and_tracts = outlines.sjoin_nearest(tracts, how='left', distance_col='centroid')


# In[133]:


blocks = gpd.read_file('../data/Census_Blocks_20231127.csv').drop(columns=['geometry'])
blocks['the_geom'] = blocks['the_geom'].apply(loads)
blocks = blocks.set_geometry('the_geom')
only_downtown['tract_block']=only_downtown['h_tract']+only_downtown['h_block']
blocks['tract_block'] = blocks['TRACTCE20']+blocks['BLOCKCE20']
g_only_downtown = gpd.GeoDataFrame(only_downtown)
merge = blocks.merge(g_only_downtown,how='inner',on='tract_block')
final = merge.groupby('the_geom').count()[['OBJECTID']].rename(columns={'OBJECTID':'count'})
final.to_csv('./output/dt_location_count_by_block.csv')


# In[140]:


tracts = gpd.read_file('../data/tracts.csv').drop(columns=['geometry'])
tracts['the_geom'] = tracts['the_geom'].apply(loads)
tracts = tracts.set_geometry('the_geom')
tracts['CT'] = tracts['CT'].str.zfill(6)


# In[147]:


only_downtown
final_tracts = tracts.merge(g_only_downtown, left_on='CT', right_on='h_tract', how='inner').groupby('the_geom').count()[['OBJECTID']].rename(columns={'OBJECTID':'count'})


# In[149]:


final_tracts.to_csv('output/dt_location_count_by_tract.csv')


# In[ ]:




