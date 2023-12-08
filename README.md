# Employment Center Analysis

By Mike Smith, Manav Dixit, Kelvin Nguyen, and Kelly Luu

## Summary

This repo contains analysis notebooks, which have been converted into python files for convenience. Each python file generates a csv file, containing some form of summary statistic or map to be visualized on the SANDAG internal platform. Some data was too large to upload to Github, so the information on where to find the data and what each file does is below:

### analysis.py

This file contains our initial analysis, as well as our first attempts to merge data and create summary statistics. It generates a dt_data.csv, which is used to visualize the Downtown SD employment center.

Required Data:

employment_center_outlines.csv - https://opendata.sandag.org/Geographic-Information-Systems/Employment-Centers-outlines-/ixp5-dfuk/about_data
tracts.csv - https://opendata.sandag.org/dataset/Census-Tracts/g3xq-yubj/about_data
ca_wac_S000_JT00_2021.csv.gz - https://lehd.ces.census.gov/data/
Census_Blocks_2020_20231117.csv - https://opendata.sandag.org/dataset/Census-Blocks/majq-4nyy
ca_wac....csv.gz - https://lehd.ces.census.gov/data/

### proximity_map.py

This file generates geospatial data, to map the homes of workers who commute to the Downtown SD employment center. It generates dt_location_count_by_tract.csv, which is used to visualize the places people commute from by Census Tract.

Required Data:

ca_od_main_JT00_2021.csv.gz - https://lehd.ces.census.gov/data/
Census_Blocks_20231127.csv - https://opendata.sandag.org/dataset/Census-Blocks/majq-4nyy
tracts.csv - https://opendata.sandag.org/dataset/Census-Tracts/g3xq-yubj/about_data
