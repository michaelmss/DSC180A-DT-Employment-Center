#!/bin/bash

# Download the required data if it does not exist

if conda env list | grep ".*dt_employment_center.*" >/dev/null 2>&1; then echo "Conda env already exists"; else conda env create --file=environment.yml -n dt_employment_center; fi

conda activate dt_employment_center

if ! test -d ./data; then
  echo "No data folder. Generating folder."
  mkdir ./data;
fi

if ! test -d ./data/large_data; then
  echo "No large_data folder. Generating folder."
  mkdir ./data/large_data;
fi
if ! test -d ./data/large_data/wac_data; then
  echo "No wac_data folder. Generating folder."
  mkdir ./data/large_data/wac_data;
fi

download () {
    if ! test -f ./data/large_data/$1; then
    echo "No $1 file. Downloading file."
    curl  -o ./data/large_data/$1 "$2";
    fi
}

download_wac () {
    if ! test -f ./data/large_data/wac_data/$1; then
    echo "No $1 file. Downloading file."
    curl  -o ./data/large_data/wac_data/$1 "$2";
    fi
}
download_small () {
    if ! test -f ./data/$1; then
    echo "No $1 file. Downloading file."
    curl  -o ./data/$1 "$2";
    fi
}

download "tracts.csv" "https://opendata.sandag.org/api/views/g3xq-yubj/rows.csv?date=20231211&accessType=DOWNLOAD"
download "ca_od_main_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/od/ca_od_main_JT00_2021.csv.gz"
download "Census_Blocks_20231127.csv" "https://opendata.sandag.org/api/views/bevn-aqff/rows.csv?date=20231211&accessType=DOWNLOAD"

download_small "2022_Estimates_Household_Income_by_2020_Census_Tract.csv" "https://opendata.sandag.org/api/views/x5fx-d7vu/rows.csv?date=20231211&accessType=DOWNLOAD"
download_small "2022_Estimates_Population_by_Age_by_2020_Census_Tract.csv" "https://opendata.sandag.org/api/views/p4vm-r7qt/rows.csv?date=20231211&accessType=DOWNLOAD"
download_small "employment_center_outlines.csv" "https://opendata.sandag.org/api/views/ixp5-dfuk/rows.csv?date=20231211&accessType=DOWNLOAD"
download_small "Jurisdictions.csv" "https://opendata.sandag.org/api/views/82fk-sjxb/rows.csv?date=20231211&accessType=DOWNLOAD"

download_wac "ca_wac_S000_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_S000_JT00_2021.csv.gz"
download_wac "ca_wac_SA01_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SA01_JT00_2021.csv.gz"
download_wac "ca_wac_SA02_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SA02_JT00_2021.csv.gz"
download_wac "ca_wac_SA03_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SA03_JT00_2021.csv.gz"
download_wac "ca_wac_SE01_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SE01_JT00_2021.csv.gz"
download_wac "ca_wac_SE02_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SE02_JT00_2021.csv.gz"
download_wac "ca_wac_SE03_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SE03_JT00_2021.csv.gz"
download_wac "ca_wac_SI01_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SI01_JT00_2021.csv.gz"
download_wac "ca_wac_SI02_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SI02_JT00_2021.csv.gz"
download_wac "ca_wac_SI03_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_SI03_JT00_2021.csv.gz"

# Check if output folder exists
if ! test -d ./output; then
  echo "No output folder. Generating folder."
  mkdir ./output;
fi

# Change to the directory containing the Python scripts
cd ./python;

# Run the Python scripts

echo "Running analysis.py (1/6)";
python analysis.py;
echo "Running proximity_map.py (2/6)";
python proximity_map.py;
echo "Running median_income_and_age.py (3/6)";
python median_income_and_age.py;
echo "Running race_data_creation.py (4/6)";
python race_data_creation.py;
echo "Running replication_DTCenter.py (5/6)";
python replication_DTCenter.py;
echo "Running traveling_from.py (6/6)";
python traveling_from.py;

echo "Complete! Data exported to /output";
