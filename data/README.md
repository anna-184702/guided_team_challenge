# README
## Dataset

### Building energy datasets
Obtaining accurate unbiased data about building energy usage is difficult due to privacy concerns, reporter bias and lack of data collection. No single worldwide dataset exists, however some contries conduct regular surveys of commercial/residential building energy usage. The most extensive of these datasets is the US federal government Building Performance Database (BPD) containing close to one million building energy usage records. Unfortunately geographic coverage of this dataset is too sparse to provide sufficient datapoints in different climate regimes. 

One of the component datasets of the BPD is the Commercial Buildings Energy Consumption Survey (CBECS). This dataset derives from a survey conducted approximately every five years by the US federal government. The survey aims to provide a representative overview of the ~5.6 million commercial buildings in the US, with each survey collecting detailed data from ~6,000 buildings. Importantly, these buildings are chosen to participate in the survey, elimninating biases inherrent in using only volunteered data. 

Survey data is available for the years 2012, 2003, 1999, 1997 and 1992 from https://www.eia.gov/consumption/commercial/data/2018/. Data from the most recent (2018) survey is being compiled and will be available for download at the end of 2020. This dataset contains extensive information about heating/cooling equipment, building characteristics and energy usage specifically for heating and cooling. Heating and cooling days from a 65F baseline are included for each building. Unfortunately location data is restricted to US census division for privacy reasons, precluding the use of ERA5 and similar reanalysis products to add other climate variables as predictors. 

These functions are currently set up for use with the 2012 data only (will be extended to all available years in the future). 

### Code files

helper_functions.py - data cleaning functions for the 2012 CBECS dataset
dataset_exploration.ipynb - example of reading in the dataset
