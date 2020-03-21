'''
AI4ER team challenge 2019/2020
Author: Anna Vaughan (av555@cam.ac.uk)
Date: 13/2/2020
'''

import numpy as np
import xarray as xr
from glob import glob
from itertools import chain

# module load python3
# module use /g/data3/hh5/public/modules
# module load conda/analysis3

# Making glob
years = range(2006, 2008)
#year_paths = [glob('/g/data3/ub4/era5/netcdf/surface/2T/{}/*.nc'.format(year)) for year in years]
#all_data = list(chain.from_iterable(year_paths))

# Temperature
for year in years:
    all_data = glob('/g/data3/ub4/era5/netcdf/surface/2T/{}/*.nc'.format(year))
    current_dataset = xr.open_mfdataset(all_data, chunks = {'time':10, 'latitude':100, 'longitude':100}, combine = 'by_coords')
    cropped_arr = current_dataset.sel(latitude = slice(50.0, 24.0), longitude = slice(-125.0, -65.0))
    tmax_array = cropped_arr.resample(time='1D').max()
    tmin_array = cropped_arr.resample(time='1D').min()
    tmean_array = cropped_arr.resample(time='1D').mean()
    tmax_array.to_netcdf(path = '/g/data3/r15/av3286/cyclone_shear/T2_{}_MAX.nc'.format(year))
    tmin_array.to_netcdf(path = '/g/data3/r15/av3286/cyclone_shear/T2_{}_MIN.nc'.format(year))
    tmean_array.to_netcdf(path = '/g/data3/r15/av3286/cyclone_shear/T2_{}_MEAN.nc'.format(year))
    print("Finished {}".format(year))   

# Windspeed
for year in years:
    u_data = glob('/g/data3/ub4/era5/netcdf/surface/10U/{}/*.nc'.format(year))
    v_data = glob('/g/data3/ub4/era5/netcdf/surface/10V/{}/*.nc'.format(year))
    u_dataset = xr.open_mfdataset(u_data, chunks = {'time':10, 'latitude':100, 'longitude':100}, combine = 'by_coords')
    v_dataset = xr.open_mfdataset(v_data, chunks = {'time':10, 'latitude':100, 'longitude':100}, combine = 'by_coords')
    u_dataset['total'] = np.sqrt(u_dataset.u10**2 + v_dataset.v10**2)
    total_arr = u_dataset.drop('u10')
    cropped_arr = total_arr.sel(latitude = slice(50.0, 24.0), longitude = slice(-125.0, -65.0))
    tmean_array = cropped_arr.resample(time='1D').mean()
    tmax_array = cropped_arr.resample(time='1D').max()
    tmean_array.to_netcdf(path = '/g/data3/r15/av3286/cyclone_shear/WIND_{}_MEAN.nc'.format(year))
    tmax_array.to_netcdf(path = '/g/data3/r15/av3286/cyclone_shear/WIND_{}_MAX.nc'.format(year))
    print("Finished {}".format(year))

# Dewpoint
for year in years:
    all_data = glob('/g/data3/ub4/era5/netcdf/surface/2D/{}/*.nc'.format(year))
    current_dataset = xr.open_mfdataset(all_data, chunks = {'time':10, 'latitude':100, 'longitude':100}, combine = 'by_coords')
    cropped_arr = current_dataset.sel(latitude = slice(50.0, 24.0), longitude = slice(-125.0, -65.0))
    tmax_array = cropped_arr.resample(time='1D').max()
    tmean_array = cropped_arr.resample(time='1D').mean()
    tmax_array.to_netcdf(path = '/g/data3/r15/av3286/cyclone_shear/D2_{}_MAX.nc'.format(year))
    tmean_array.to_netcdf(path = '/g/data3/r15/av3286/cyclone_shear/D2_{}_MEAN.nc'.format(year))
    print("Finished {}".format(year))  
