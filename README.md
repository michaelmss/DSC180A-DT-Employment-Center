# Employment Center Analysis

By Mike Smith, Manav Dixit, Kelvin Nguyen, and Kelly Luu

## Summary

This repo contains analysis notebooks, which have been converted into python files for convenience. Each python file generates a csv file, containing some form of summary statistic or map to be visualized on the SANDAG internal platform.

The Output can be re-generated by running the run.py file while using the conda environment specified in environment.yml.

Before running run.py, ensure that your environment is correct and the necessary data has been downloaded from the Census Bureau and the SANDAG Open Data Portal

## Conda Environment

Generate the needed conda environment by running the following command:

```
conda env create --name envname --file=environments.yml
```

## Required Data Sources

The following data needs to be downloaded and added to the data/ folder before running run.py:
