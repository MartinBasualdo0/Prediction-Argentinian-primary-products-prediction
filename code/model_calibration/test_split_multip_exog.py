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

start_time = time.time()
models_params = {
    'pre': {
        "max_p" : 9,
        "max_q" : 9,
        "existe_estacionalidad": True,
        "transform_log": True
    },
    'ip': {
        "max_p" : 9,
        "max_q" : 9,
        "existe_estacionalidad": True,
        "transform_log": False
    },
    'itcr': {
        "max_p" : 9,
        "max_q" : 9,
        "existe_estacionalidad": False,
        "transform_log": False
    }
}

df = DataModelPreparation(meses_prediccion=0, meses_testeo=0).test_df # A corregir

def agrega_fila_datos_modelo(args) -> pd.DataFrame:
    start_time_model = time.time()
    variable, existe_estacionalidad, transform_log, p, d, q, P, D, Q, M = args
    tscv = TimeSeriesSplit(n_splits = 5)
    RMSE_list = []
    MSE_list = []
    seasonal_order = (P,D,Q,M) if existe_estacionalidad else (0,0,0,0)  # provide a default value
    for train_index, test_index in tscv.split(df):
        cv_train, cv_test = df.iloc[train_index],df.iloc[test_index]
        y = np.log(cv_train[variable] + 1) if transform_log else cv_train[variable]
        meses_prediccion = cv_test.shape[0]
        sarima_exog = SARIMAX(y, order = (p,d,q), seasonal_order=seasonal_order)
        try:
            model_fit = sarima_exog.fit(maxiter=20_000, disp = False, method_kwargs= {"warn_convergence": False})
            predictions = model_fit.forecast(meses_prediccion)
            mse_split = mean_squared_error(cv_test[variable], predictions)
            rmse_split = sqrt(mse_split)  
            RMSE_list.append(rmse_split)
            MSE_list.append(mse_split)
        except Exception as e:
            print(f"Failed to fit model {p,d,q,Q,D,Q,M} for variable {variable}. Error: {e}")
            RMSE_list = "error"
            MSE_list = "error"
    RMSE = np.mean(RMSE_list) if RMSE_list != "error" else "error"
    MSE = np.mean(MSE_list) if MSE_list != "error" else "error"
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
        'MSE': MSE,
        'RMSE':RMSE,
        'time' : elapsed_time_model
    }
    print(new_row)
    return new_row
    
if __name__ == "__main__":
    for modelo in models_params:
        max_p = models_params[modelo]["max_p"]
        max_q = models_params[modelo]["max_q"]
        variable =  modelo
        existe_estacionalidad =  models_params[modelo]["existe_estacionalidad"]
        transform_log =  models_params[modelo]["transform_log"]
        M = 12 if existe_estacionalidad else 1
        calibration_df = pd.DataFrame(columns=['variable', 'p', 'd', 'q', 'P', 'D', 'Q', 'M','MSE_split_1','MSE_split_2','MSE_split_3','MSE_split_4','MSE_split_5','MSE','RMSE'])
        
        pool = mp.Pool(mp.cpu_count())
        args = [(variable, existe_estacionalidad, transform_log, p, d, q, P, D, Q, M) for p in range(0,max_p+1) for d in range(0,2) for q in range(0,max_q+1) for P in range(0,2) for D in range(0,2) for Q in range(0,2)]
        results = pool.map(agrega_fila_datos_modelo, args)
        results = pd.DataFrame(results)
        print(f"Resultado del pool:\n",results)
        pool.close()
        
        print(f"Calibration of {variable} terminada!!!")
        # calibration_df = pd.DataFrame(results, columns=['variable', 'p', 'd', 'q', 'P', 'D', 'Q', 'M','MSE_split_1','MSE_split_2','MSE_split_3','MSE_split_4','MSE_split_5','MSE','RMSE']) 
        # calibration_df.to_excel(f"./data/test/calibration_{variable}.xlsx", index=False)
        results.to_excel(f"./data/test/calibration_{variable}.xlsx", index=False)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print(f"The script took {int(minutes)} minutes and {seconds:.0f} seconds to run.")