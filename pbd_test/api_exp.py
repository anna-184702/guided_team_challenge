from bpd_api_python_lib import *

# Want to get the mean site EUI 

# Set up filtering by zip code/whatever
filters = {"building_class": ["Commercial"], "site_eui"}

filters = {"site_year": {"min": 2018.0,"max":2018.0}}

# Call histogram to get EUI stats of filtered buildings
eui_dict = histogram(group_by = ["site_eui"], filters=filters)
print(np.cumsum(eui_dict['counts'])[-1])
eui_stats = eui_dict["totals"]
eui_mean = eui_stats["mean"]
percentile_0 = eui_stats["percentile_0"]
percentile_25 = eui_stats["percentile_25"]
percentile_50 = eui_stats["percentile_50"]
percentile_75 = eui_stats["percentile_75"]
percentile_100 = eui_stats["percentile_100"]
sigma_eui = eui_stats["standard_deviation"]

nums = np.linspace(2012, 2012.12, 13)
for i in range(12):
    print(i)
    filters = {"site_year": {"min": nums[i],"max":nums[i+1]}}
    eui_dict = histogram(group_by = ["site_year"], filters=filters)
    print(np.cumsum(eui_dict['counts'])[-1])

filters = {"site_year": {"min": 2012.2,"max":2012.3}, "zip_code":["10001"], "building_type"}
no_data = histogram(group_by = ["site_eui"], filters=filters)
eui_dict


