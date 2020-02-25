import numpy as np 
import pandas as pd 

def data_target_ELHTBTU(path_to_dataset):
    '''
    Read in all relevant predictors as a dataframe and targets as a 
    separate series
    Parameters:
    ----------
    path_to_dataset (string):
        Path to the CBECS dataset to read in

    Returns:
    --------
    data (pandas.DataFrame):
        Predictor array
    target_heating_elec (pandas.Series):
        Heating target
    target_cooling_elec (pandas.Series):
        Cooling target
    '''

    data = pd.read_csv(path_to_dataset)

    # Delete any predictor without data for >90% of buildings
    nan_sums = data.isna().sum()
    drop_count = 0
    dropped_keys = []
    for key in data.keys():
        if nan_sums[key]/6719 > 0.1:
            data.drop([key], inplace = True, axis = 1)
            drop_count+=1
            dropped_keys.append(key)

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
    
    data.drop(['PUBID', 'PUBCLIM', 'MFUSED', 'MFBTU', 'MFEXP', 'ELCNS', 'ELBTU', 
        'ELEXP', 'NGCNS', 'NGBTU', 'NGEXP', 'FKCNS', 'FKBTU', 'FKEXP', 'PUBID'],
         inplace = True, axis = 1)

    # Separate out the target column
    data = data[data['ELHT1']==1]

    # lets just drop the nans since they mess up XGB
    data.dropna(inplace = True)

    target_heating_elec = data['ELHTBTU']
    target_cooling_elec = data['ELCLBTU']
    data.drop(['ELHTBTU', 'ELCLBTU'], inplace = True, axis = 1)

    data.drop(['ELHTBTU', 'ELCLBTU'], inplace = True, axis = 1)

    return (data.reindex(), target_heating_elec, target_cooling_elec)


def data_all(path_to_dataset):
    '''
    Function to read in all relevant predictors as a dataframe
    Parameters:
    ----------
    path_to_dataset (string):
        Path to the CBECS dataset to read in

    Returns:
    --------
    data (pandas.DataFrame):
        All predictors
    '''

    data = pd.read_csv(path_to_dataset)

    # Delete any predictor without data for >90% of buildings
    nan_sums = data.isna().sum()
    drop_count = 0
    dropped_keys = []
    for key in data.keys():
        if nan_sums[key]/6719 > 0.1:
            data.drop([key], inplace = True, axis = 1)
            drop_count+=1
            dropped_keys.append(key)

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

    return data
