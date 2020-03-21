import numpy as np 
import pandas as pd 
from glob import glob

print("ok")

def drop_nan_ps(data_frame):
    # Delete any predictor without data for >90% of buildings
    nan_sums = data_frame.isna().sum()
    for key in data_frame.keys():
        if nan_sums[key]/len(data_frame) > 0.05:
            data_frame.drop([key], inplace = True, axis = 1)
    return data_frame


# EXPERIMENTS - CBECS
# 1. Play around with how the nans are removed - whether they are dropped 
#   after predictor filtering or just set to minus one
# 2. Experiment with different models for different building types
# 3. Different models for different heating types

# EXPERIMENTS - RBECS

#--------------------
#####################
# Import the files
#####################
#--------------------

cbecs_data = pd.read_csv('cbecs_2003_2012.csv')
rbecs_data = pd.read_csv('rbecs_2005_2009_2015.csv')

for key in cbecs_data.keys():
    cbecs_data[key] = pd.to_numeric(cbecs_data[key], errors = "coerce")

for key in rbecs_data.keys():
    rbecs_data[key] = pd.to_numeric(rbecs_data[key], errors = "coerce")

#---------------------
######################
# Make CBECS datasets
######################
#---------------------

# Drop the common predictors
cbecs_data.drop(['Unnamed: 0'], inplace = True, axis = 1)

# A bunch of predictors thst we don't require

nn_predictors = ['SQFTC', 'REGION', 'CENDIV', 'YRCONC', 'PBAPLUS', 'NOCCAT']
cbecs_data.drop([p for p in nn_predictors if p in cbecs_data.keys()], axis = 1, inplace = True)
cbecs_data['FREESTN'][cbecs_data['FREESTN'].isna()] = 0

new_labels = {old_key:old_key.strip() for old_key in cbecs_data.keys()}
cbecs_data.rename(new_labels, inplace = True, axis = 1)

total_heating_use = cbecs_data['MFHTBTU']
elec_heating_use = cbecs_data['ELHTBTU']
dh_heating_use = cbecs_data['DHHTBTU']
ng_heating_use = cbecs_data['FKHTBTU']
elec_cooling_use = cbecs_data['ELCLBTU']

# Other than this, drop all the energy used
energy_keys = [key for key in cbecs_data.keys() if key[-3:]=="BTU"]
cbecs_data.drop(energy_keys, inplace = True, axis = 1)

# Total heating use (dataset not split by major fuel type)
#predictors = cbecs_data[cbecs_data['HT1'] == 1]
#total_heating_use = total_heating_use[cbecs_data['HT1'] == 1]
#predictors.to_csv("total_heating_all_predictors.csv")
#total_heating_use.to_csv("total_heating_use_targets.csv")

# Electricity cooling use 
cbecs_elec_cool = cbecs_data[cbecs_data['ELCOOL']==1]
elec_cooling_use = elec_cooling_use[cbecs_elec_cool.index]
elec_cooling = cbecs_elec_cool[~elec_cooling_use.isna()]
elec_cooling_use = elec_cooling_use[~elec_cooling_use.isna()]

elec_cooling = drop_nan_ps(elec_cooling)

for key in elec_cooling.keys():
    elec_cooling[key][elec_cooling[key].isna()] = -1

elec_cooling.to_csv("elec_cooling_all_predictors.csv")
elec_cooling_use.to_csv("elec_cooling_use_targets.csv")

# Electricity heating use
cbecs_elec_heat = cbecs_data[cbecs_data['ELHT1']==1]
elec_heating_use = elec_heating_use[cbecs_elec_heat.index]
elec_heating = cbecs_elec_heat[~elec_heating_use.isna()]
elec_heating_use = elec_heating_use[~elec_heating_use.isna()]

elec_heating = drop_nan_ps(elec_heating)

for key in elec_heating.keys():
    elec_heating[key][elec_heating[key].isna()] = -1

elec_heating.to_csv("elec_heating_all_predictors.csv")
elec_heating_use.to_csv("elec_heating_use_targets.csv")

# Natural gas heating use
cbecs_ng_heat = cbecs_data[cbecs_data['NGHT1']==1]
ng_heating_use = ng_heating_use[cbecs_ng_heat.index]
ng_heating = cbecs_ng_heat[~ng_heating_use.isna()]
ng_heating_use = ng_heating_use[~ng_heating_use.isna()]

ng_heating = drop_nan_ps(ng_heating)

for key in ng_heating.keys():
    ng_heating[key][ng_heating[key].isna()] = -1

ng_heating.to_csv("ng_heating_all_predictors.csv")
ng_heating_use.to_csv("ng_heating_use_targets.csv")

# District heat heating use
cbecs_dh_heat = cbecs_data[cbecs_data['DHHT1']==1]
dh_heating_use = dh_heating_use[cbecs_dh_heat.index]
dh_heating = cbecs_dh_heat[~dh_heating_use.isna()]
dh_heating_use = dh_heating_use[~dh_heating_use.isna()]

dh_heating = drop_nan_ps(dh_heating)

for key in dh_heating.keys():
    dh_heating[key][dh_heating[key].isna()] = -1

dh_heating.to_csv("dh_heating_all_predictors.csv")
dh_heating_use.to_csv("dh_heating_use_targets.csv")

#---------------------
######################
# Make RBECS datasets
######################
#---------------------

drop_p = ['DOEID', 'REGIONC', 'DIVISION', 'METROMICRO', 'Unnamed: 0']
rbecs_data.drop(drop_p, axis = 1, inplace = True)

rbecs_datah = rbecs_data[rbecs_data['TOTHSQFT'] != 0]
rbecs_datac = rbecs_data[rbecs_data['TOTCSQFT'] != 0]

elec_heating_use = rbecs_datah['KWHSPH']
ng_heating_use = rbecs_datah['BTUNGSPH']
elec_cooling_use = rbecs_datac['KWHCOL']
# Need electricity for cooling, electricity and natural gas for heating
# Electricity usage for space heating KWHSPH/ cooling KWHCOL
# Drop all the other KW prefixes and the BTU, DOL prefixes
# Natural gas for heating BTUNGSPH, drop all CUFEE, GALL, TOTAL

drop_keys = [key 
            for key in rbecs_data.keys() 
                if key.startswith(('BTU', 'DOL', 'CUFEE', 'GALL', 'TOTAL', 'KW'))]

rbecs_datac.drop(drop_keys, inplace = True, axis = 1)
rbecs_datah.drop(drop_keys, inplace = True, axis = 1)


# Natural gas heating use
rbecs_ng_heat = rbecs_datah[rbecs_datah['FUEL_HEAT']==1]
ng_heating_use = ng_heating_use[rbecs_ng_heat.index]
ng_heating = rbecs_ng_heat[~ng_heating_use.isna()]
ng_heating_use = ng_heating_use[~ng_heating_use.isna()]

ng_heating = drop_nan_ps(ng_heating)

for key in ng_heating.keys():
    ng_heating[key][ng_heating[key].isna()] = -1

ng_heating.to_csv("res_ng_heating_all_predictors.csv")
ng_heating_use.to_csv("res_ng_heating_use_targets.csv")

# Electric heating use
rbecs_elec_heat = rbecs_datah[rbecs_datah['FUEL_HEAT']==5]
elec_heating_use = elec_heating_use[rbecs_elec_heat.index]
elec_heating = rbecs_elec_heat[~elec_heating_use.isna()]
elec_heating_use = elec_heating_use[~elec_heating_use.isna()]

elec_heating = drop_nan_ps(elec_heating)

for key in elec_heating.keys():
    elec_heating[key][elec_heating[key].isna()] = -1

elec_heating.to_csv("res_elec_heating_all_predictors.csv")
elec_heating_use.to_csv("res_elec_heating_use_targets.csv")

# Electricity cooling use 
rbecs_elec_cool = rbecs_datac[rbecs_datac['ELCOOL']==1]
elec_cooling_use = elec_cooling_use[rbecs_elec_cool.index]
elec_cooling = rbecs_elec_cool[~elec_cooling_use.isna()]
elec_cooling_use = elec_cooling_use[~elec_cooling_use.isna()]

elec_cooling = drop_nan_ps(elec_cooling)

for key in elec_cooling.keys():
    elec_cooling[key][elec_cooling[key].isna()] = -1

elec_cooling.to_csv("res_elec_cooling_all_predictors.csv")
elec_cooling_use.to_csv("res_elec_cooling_use_targets.csv")


