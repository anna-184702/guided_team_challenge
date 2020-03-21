import numpy as np 
import pandas as pd 
from sklearn.feature_selection import SelectKBest, chi2, mutual_info
import xgboost
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import shap

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

data = pd.read_csv("2012_data.csv")
print("CBECS total predictors = {}".format(len(data.keys())))

data.drop(['PUBCLIM', 'MFUSED', 'MFBTU', 'MFEXP', 'ELCNS', 'ELBTU', 'ELEXP', 
            'NGCNS', 'NGBTU', 'NGEXP', 'FKCNS', 'FKBTU', 'FKEXP', 'PUBID'], inplace = True, axis = 1)


# Delete any column without data for >90% of buildings
nan_sums = data.isna().sum()
drop_count = 0
dropped_keys = []
for key in data.keys():
    if nan_sums[key]/6719 > 0.1:
        data.drop([key], inplace = True, axis = 1)
        drop_count+=1
        dropped_keys.append(key)


print("Number of predictors dropped = {}".format(drop_count))

# Drop irrelevant predictors
for key in data.keys():
    if key[0] == 'Z':
        data.drop([key], inplace = True, axis = 1)
    elif key not in ['ELHTBTU', 'ELCLBTU']and key[-3:] == 'BTU':
        data.drop([key], inplace = True, axis = 1)
    elif key[:5] == 'FINAL':
        data.drop([key], inplace = True, axis = 1)
    elif key[:3] == "DHH":
        data.drop([key], inplace = True, axis = 1)

# 150 predictors remain :) 

#'HDD65', 'CDD65'

# Because I am too lazy to figure out what is wrong, lets just drop the nans
data.dropna(inplace = True)

# Now we want to do the feature selection
# Separate out the target column
target_heating_elec = data['ELHTBTU']
target_cooling_elec = data['ELCLBTU']
data.drop(['ELHTBTU', 'ELCLBTU'], inplace = True, axis = 1)

# Dummy baseline
clf = DummyRegressor(strategy='mean')
clf.fit(data, target_heating_elec)
Y_f = clf.predict(data)

print("MSE baseline = {}".format(mean_squared_error(target_heating_elec, Y_f)))

# Time to build a model

# Train - test split
x_train, x_test, y_train, y_test = train_test_split(data, target_heating_elec, test_size=0.2, random_state=5)

MAX_DEPTH = 4
N_ESTIMATORS = 100
model = xgboost.XGBRegressor(max_depth=MAX_DEPTH, n_estimators=N_ESTIMATORS)
model.fit(x_train, y_train, verbose = True)
y_pred = model.predict(x_test)
print("MSE baseline = {}".format(mean_squared_error(target_heating_elec, Y_f)))

# SHAP tree explainers 
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(data)
shap.summary_plot(shap_values,data)





