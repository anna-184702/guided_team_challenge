import numpy as np 
import pandas as pd 
from glob import glob

def write_lim_pred_dataset(fuel_type, cool_heat, res = False):

    if not res:
        csv_path = fuel_type+'_'+cool_heat+'_all_predictors.csv'
    else:
        csv_path = 'res_'+fuel_type+'_'+cool_heat+'_all_predictors.csv'

    data = pd.read_csv(csv_path)
    if not res:
        data = data[['SQFT', 'PBA', 'HDD65', 'CDD65']]
        data.to_csv(fuel_type+'_'+cool_heat+'_lim_predictors.csv')
    else:
        data = data[['STORIES', 'TYPEHUQ', 'TOTHSQFT', 'TOTCSQFT', 'HDD65', 'CDD65']]
        data.to_csv('res_'+fuel_type+'_'+cool_heat+'_lim_predictors.csv')

if __name__ == "__main__":
    
    res_params = [('ng', 'heating'), ('elec', 'heating'), ('elec', 'cooling')]
    for p in res_params:
        write_lim_pred_dataset(*p, res = True)

    com_params = [('ng', 'heating'), ('elec', 'heating'), ('dh', 'heating'), ('elec', 'cooling')]
    for p in com_params:
        write_lim_pred_dataset(*p)