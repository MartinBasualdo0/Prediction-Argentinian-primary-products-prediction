import pandas as pd
from sarima_model_preparation import DataModelPreparation
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error as mean_squared_error
import time
import numpy as np
from math import sqrt
from sklearn.model_selection import TimeSeriesSplit
import multiprocessing as mp
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)
warnings.simplefilter('ignore', FutureWarning)
warnings.simplefilter('ignore', UserWarning)

n_splits = 5

max_p = 9
max_q = 9
M=12
# df = DataModelPreparation(meses_prediccion=0, meses_testeo=0).test_df #A corregir
df = pd.read_excel("data/data.xlsx")
variable = "pp"
seasonality_exists = True
transform_log = False
X = ["er_cp", "pi", "pre", "gap"]
calibration_df = pd.DataFrame(columns=['variable', 'p', 'd', 'q', 'P', 'D', 'Q', 'M',
                                       'MSE_split_1','MSE_split_2','MSE_split_3','MSE_split_4','MSE_split_5',
                                       'MSE','RMSE'])

def add_row_model_data(args):
    start_time_model = time.time()
    variable, seasonality_exists, transform_log, p, d, q, P, D, Q, M = args
    tscv = TimeSeriesSplit(n_splits = n_splits)
    RMSE_list = []
    MSE_list = []
    AIC_list = []
    seasonal_order = (P,D,Q,M) if seasonality_exists else (0,0,0,0)  # provide a default value
    for train_index, test_index in tscv.split(df):
        cv_train, cv_test = df.iloc[train_index],df.iloc[test_index]
        y = np.log(cv_train[variable] + 1) if transform_log else cv_train[variable]
        meses_prediccion = cv_test.shape[0]
        sarima_exog = SARIMAX(y, order = (p,d,q),exog=cv_train[X], seasonal_order=seasonal_order)
        try:
            model_fit = sarima_exog.fit(maxiter=20_000, disp = False, method_kwargs= {"warn_convergence": False})
            predictions = model_fit.forecast(meses_prediccion, exog = cv_test[X])
            aic_split = model_fit.aic
            predictions = np.exp(predictions) if transform_log else predictions #Ahora debería de estar mejor
            mse_split = mean_squared_error(cv_test[variable], predictions)
            rmse_split = sqrt(mse_split)  
            RMSE_list.append(rmse_split)
            MSE_list.append(mse_split)
            AIC_list.append(aic_split) 
        except Exception as e:
            print(f"Failed to fit model {p,d,q,Q,D,Q,M} for variable {variable}. Error: {e}")
            RMSE_list = "error"
            MSE_list = "error"
            AIC_list = "error"  
    RMSE = np.mean(RMSE_list) if RMSE_list != "error" else "error"
    MSE = np.mean(MSE_list) if MSE_list != "error" else "error"
    AIC = np.mean(AIC_list) if AIC_list != "error" else "error"

    end_time_model = time.time()
    elapsed_time_model = end_time_model - start_time_model
    new_row = {
        'variable': variable,
        'p': p,
        'd': d,
        'q': q,
        'P': P,
        'D': D,
        'Q': Q,
        'M': M,
        'MSE_split_1': MSE_list[0] if MSE_list !="error" else "error",
        'MSE_split_2': MSE_list[1] if MSE_list !="error" else "error",
        'MSE_split_3': MSE_list[2] if MSE_list !="error" else "error",
        'MSE_split_4': MSE_list[3] if MSE_list !="error" else "error",
        'MSE_split_5': MSE_list[4] if MSE_list !="error" else "error",
        'AIC_split_1': AIC_list[0] if AIC_list !="error" else "error",
        'AIC_split_2': AIC_list[1] if AIC_list !="error" else "error",
        'AIC_split_3': AIC_list[2] if AIC_list !="error" else "error",
        'AIC_split_4': AIC_list[3] if AIC_list !="error" else "error",
        'AIC_split_5': AIC_list[4] if AIC_list !="error" else "error",
        'AIC' : AIC,
        'MSE': MSE,
        'RMSE':RMSE,
        'time': elapsed_time_model
    }
    print(new_row)
    return new_row
    
if __name__ == '__main__':
    start_time = time.time()
    pool = mp.Pool(mp.cpu_count())
    args = [(variable, seasonality_exists, transform_log, p, d, q, P, D, Q, M) for p in range(0,max_p+1) for d in range(0,2) for q in range(0,max_q+1) for P in range(0,2) for D in range(0,2) for Q in range(0,2)]
    results = pool.map(add_row_model_data, args)
    results = pd.DataFrame(results)
    pool.close()
    results.to_excel(f"./data/calibration_sarimax_{n_splits}_splits_aic/calibration_{variable}.xlsx", index=False)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"The script took {int(minutes)} minutes and {seconds:.0f} seconds to run.")