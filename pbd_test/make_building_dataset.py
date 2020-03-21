'''
AI4ER team challenge 2019/2020
Author: Anna Vaughan (av555@cam.ac.uk)
Date: 14/2/2020
'''

import numpy as np 
import xarray as xr
import pandas as pd

from glob import glob
from bpd_api_python_lib import *
from zip_to_lat_lon import *

def get_quantiles(timeseries):
    quantiles = [0.99, 0.95, 0.90, 0.75, 0.25, 0.10, 0.05, 0.01]
    euis = []
    for q in quantiles:
        euis.append(timeseries.quantile(q))
    return(euis)

# Read in the climate variable data

# 9417 unique lat/lon points

# initialise dataframe and arrays
year_times = np.linspace(2006.0, 2016, 121)
zip_dict = make_zip_dict()
print("ZIP dictionary completed")

building_types = ['Commercial', 'Residential']

quantiles = [99, 95, 90, 75, 25, 10, 5, 1]
T_max_quantiles = ['T_max_'+str(i) for i in quantiles]
T_mean_quantiles = ['T_mean_'+str(i) for i in quantiles]
T_min_quantiles = ['T_min_'+str(i) for i in quantiles]
D_max_quantiles = ['D_max_'+str(i) for i in quantiles]
D_mean_quantiles = ['D_mean_'+str(i) for i in quantiles]

# Need to add wind and comfort index
data_columns = ['Latitude', 'Longitude', 'year', 'month', 'building_type', 
                'T_max_99', 'T_max_95', 'T_max_90', 'T_max_75', 'T_max_25', 'T_max_10', 'T_max_5', 'T_max_1',
                'T_mean_99', 'T_mean_95', 'T_mean_90', 'T_mean_75', 'T_mean_25', 'T_mean_10', 'T_mean_5', 'T_mean_1',
                'T_min_99', 'T_min_95', 'T_min_90', 'T_min_75', 'T_min_25', 'T_min_10', 'T_min_5', 'T_min_1',
                'D_max_99', 'D_max_95', 'D_max_90', 'D_max_75', 'D_max_25', 'D_max_10', 'D_max_5', 'D_max_1',
                'D_mean_99', 'D_mean_95', 'D_mean_90', 'D_mean_75', 'D_mean_25', 'D_mean_10', 'D_mean_5', 'D_mean_1',
                'eui_mean', 'eui_sigma']

data_index = np.array(range(0, len(zip_dict.keys())))

dataset = pd.DataFrame(index=data_index, columns=data_columns)

df_count = 0

t_min_data = xr.open_mfdataset(glob("T2/min/*.nc"), combine = 'by_coords')
t_mean_data = xr.open_mfdataset(glob("T2/mean/*.nc"), combine = 'by_coords')
t_max_data = xr.open_mfdataset(glob("T2/max/*.nc"), combine = 'by_coords')
d_mean_data = xr.open_mfdataset(glob("D2/mean/*.nc"), combine = 'by_coords')
d_max_data = xr.open_mfdataset(glob("D2/max/*.nc"), combine = 'by_coords')

total_data = t_mean_data
total_data['t_mean'] = t_mean_data['t2m']
total_data['t_min'] = t_min_data['t2m']
total_data['t_max'] = t_max_data['t2m']
total_data['d_mean'] = d_mean_data['d2m']
total_data['d_max'] = d_max_data['d2m']
total_data = total_data.compute()

for location in zip_dict.keys():
    # Skip the weird cases
    if type(location) != tuple:
        continue
    
    # Get the list of associated ZIP codes
    current_zip_list = [str(i) for i in zip_dict[location]]
    print("Location")

    # Load the climate data timeseries for the point
    print(location)
    total_timeseries = total_data.sel(latitude = location[0], longitude = location[1])

    for ind in range(120):
        # 121 values

        start_year_month = year_times[ind]
        end_year_month = year_times[ind+1]

        string_year_start = int(start_year_month)
        string_month_start = int(np.round((start_year_month%1)*12))

        print(string_year_start)
        print(string_month_start)

        for building_type in building_types:

            # Set up API filters
            filters = {"building_class": [building_type],
                "site_year": {"min": start_year_month, "max": end_year_month},
                "zip_code": current_zip_list, 
                }

            # Make API request
            eui_dict = histogram(group_by = ["electric_eui"], filters=filters)

            # Get data out
            if eui_dict['metadata']['message'] == 'success' and eui_dict['totals']['number_of_matching_buildings'] != 0:

                print("YES")

                mean = eui_dict['totals']['mean']
                sigma = eui_dict['totals']['standard_deviation']

                dataset.iloc[df_count][['Latitude', 'Longitude']] = location
                dataset.iloc[df_count][['year', 'month', 'building_type']] = [string_year_start, string_month_start, building_type]

                dataset.iloc[df_count][T_mean_quantiles] = get_quantiles(total_data.t_mean)
                dataset.iloc[df_count][T_max_quantiles] = get_quantiles(total_data.t_max)
                dataset.iloc[df_count][T_min_quantiles] = get_quantiles(total_data.t_min)
                dataset.iloc[df_count][D_max_quantiles] = get_quantiles(total_data.d_mean)
                dataset.iloc[df_count][D_mean_quantiles] = get_quantiles(total_data.d_max)

                dataset.iloc[df_count][['eui_mean', 'eui_sigma']] = [mean, sigma]

                # In case of crashes, write out to CSV every 100 lines
                if df_count%100 == 0:
                    dataset.to_csv("dataset_csv_backup.csv")

            df_count += 1