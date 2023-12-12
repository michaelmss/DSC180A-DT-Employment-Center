# Employment Center Analysis

By Mike Smith, Manav Dixit, Kelvin Nguyen, and Kelly Luu

## Summary

This repo contains python files which generate data to be visualized on SANDAG's internal data visualization platform.

The Output csv files can be re-generated to the output/ folder by running the run.sh file while using the conda environment specified in environment.yml.

## To generate the export

### Activate your Conda environment.

This file will download the required data, and generate the exports to the output/ folder. Anaconda needs to be installed and configured before running this script.

To create a conda environment compatable with our code, run `conda env create --file=environment.yml -n dt_employment_center` in the root directory of this project.

Then, to activate it, run `conda activate dt_employment_center`

### Run the run.sh file

Simply run `sh run.sh` on Mac, or `bash run.sh` on windows.

This may take awhile to run, as it will download all required dependencies, data, and execute python code.
