# Import libraries
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.metrics import mean_squared_error, make_scorer


# Define the grid search loss
def rmse_loss(y_true, y_pred):
    return mean_squared_error(y_true, y_pred, squared = False)

def grid_search_xgbr(predictors, targets, unique_depths, unique_n_estimators):
    my_scorer = make_scorer(rmse_loss)
    gsCV = GridSearchCV(estimator=RandomForestRegressor(),
                param_grid={'max_depth': unique_depths, 'n_estimators': unique_n_estimators}, 
                scoring = my_scorer,
                cv = 2,
                verbose = 100)

    gsCV.fit(predictors, targets)
    return gsCV

def plot_gs_results(gsCV, unique_depths, unique_n_estimators):
    depths = gsCV.cv_results_['param_max_depth']
    scores = gsCV.cv_results_['mean_test_score']

    for depth in unique_depths:
        depth_constant_scores = scores[depths == depth]
        plt.plot(unique_n_estimators, depth_constant_scores, label = depth)

    plt.legend(loc = "lower right")

    plt.show()


def get_targets_predictors(cool_heat, fuel_type, res = False, lim = False):
    '''
    Read in the required datasets
    Parameters:
    -----------
    cool_heat: String
        either 'cooling' or 'heating'
    fuel_type: String
        either 'elec', 'ng', 'dh'
    res: Bool
        True for residential 
    Returns:
    --------
    predictors: pd.Dataframe
        model predictors
    targets: pd.Dataframe
        model targets
    '''

    if res:
        predictor_file_path = 'res_'+fuel_type+'_'+cool_heat+'_all_predictors.csv'
        target_file_path = 'res_'+fuel_type+'_'+cool_heat+'_use_targets.csv'
    elif lim:
        predictor_file_path = fuel_type+'_'+cool_heat+'_lim_predictors.csv'
        target_file_path = fuel_type+'_'+cool_heat+'_use_targets.csv'
    elif res and lim:
        predictor_file_path = 'res_'+fuel_type+'_'+cool_heat+'_lim_predictors.csv'
        target_file_path = 'res_'+fuel_type+'_'+cool_heat+'_use_targets.csv'
    else:
        predictor_file_path = fuel_type+'_'+cool_heat+'_sall_predictors.csv'
        target_file_path = fuel_type+'_'+cool_heat+'_use_targets.csv'

    predictors = pd.read_csv('../make_data_files/'+predictor_file_path)
    targets = pd.read_csv('../make_data_files/'+target_file_path, header = None)

    # Fix up the indexing
    ind_keys = [key for key in predictors.keys() if key.startswith('Unnamed')]
    predictors.drop(ind_keys, axis = 1, inplace = True)
    targets.drop([0], axis = 1, inplace = True)

    # Convert to KWH
    if (not res) or fuel_type == "ng":
        targets = targets/3.412

    # Normalise by SQFT for commercial
    if not res:
        targets[1] = targets[1]/predictors['SQFT']
    else:
        if cool_heat == 'cooling':
            targets[1] = targets[1]/predictors['TOTHSQFT']
        else:
            targets[1] = targets[1]/predictors['TOTCSQFT']

    # Get rid of the infinite values
    predictors = predictors[np.isfinite(targets[1])]
    targets = targets[np.isfinite(targets[1])]

    # Scale the features
    sc = StandardScaler()
    predictors = sc.fit_transform(predictors)

    return predictors, targets