import pandas as pd
from sarima_model_preparation import DataModelPreparation
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error as mean_squared_error
import time
import numpy as np
from math import sqrt
from sklearn.model_selection import TimeSeriesSplit

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

def agrega_fila_datos_modelo(calibration_df: pd.DataFrame, variable: str, existe_estacionalidad:bool, transform_log:bool,p:int,d:int,q:int,
                             P:int=None, D:int=None, Q:int=None, M:int=None):
    tscv = TimeSeriesSplit(n_splits = 5)
    RMSE = []
    MSE = []
    seasonal_order = (P,D,Q,M) if existe_estacionalidad else (0,0,0,0)  # provide a default value
    for train_index, test_index in tscv.split(df):
        cv_train, cv_test = df.iloc[train_index],df.iloc[test_index]
        y = np.log(cv_train[variable] + 1) if transform_log else cv_train[variable]
        meses_prediccion = cv_test.shape[0]
        sarima_exog = SARIMAX(y, order = (p,d,q), seasonal_order=seasonal_order)
        try:
            model_fit = sarima_exog.fit(maxiter=20_000)
            predictions = model_fit.forecast(meses_prediccion)
            mse_split = mean_squared_error(cv_test[variable], predictions)
            rmse_split = sqrt(mse_split)  
            RMSE.append(rmse_split)
            MSE.append(mse_split)
        except Exception as e:
            print(f"Failed to fit model {p,d,q,Q,D,Q,M} for variable {variable}. Error: {e}")
            RMSE = "error"
            MSE = "error"
    RMSE = np.mean(RMSE) if RMSE != "error" else "error"
    MSE = np.mean(MSE) if MSE != "error" else "error"
    new_row = {
        'variable': variable,
        'p': p,
        'd': d,
        'q': q,
        'P': P,
        'D': D,
        'Q': Q,
        'M': M,
        'MSE': MSE,
        'RMSE':RMSE
    }
    calibration_df.loc[len(calibration_df)] = new_row
   
   
for modelo in models_params:
    print(modelo, "Empieza!")
    start_time = time.time()
    max_p = models_params[modelo]["max_p"]
    max_q = models_params[modelo]["max_q"]
    variable =  modelo
    existe_estacionalidad =  models_params[modelo]["existe_estacionalidad"]
    transform_log =  models_params[modelo]["transform_log"]

    calibration_df = pd.DataFrame(columns=['variable', 'p', 'd', 'q', 'P', 'D', 'Q', 'M', 'MSE', 'RMSE'])
    for p in range(0,max_p+1):
        for d in range(0,2):
            for q in range(0,max_q+1):
                if existe_estacionalidad:   
                    for P in range(0,2):
                        for D in range(0,2):
                            for Q in range(0,2):
                                print("MODELO!!!",modelo,p,d,q,P,D,Q)
                                agrega_fila_datos_modelo(calibration_df, variable, existe_estacionalidad, transform_log,
                                                        p,d,q,
                                                        P,D,Q,M=12)
                else:
                    agrega_fila_datos_modelo(calibration_df, variable, existe_estacionalidad, transform_log,
                                            p,d,q)
                                

            
    calibration_df = calibration_df.drop_duplicates()  
    calibration_df.to_excel(f"./data/calibration_sarimax_split/calibration_{variable}.xlsx", index=False)
    print(modelo, "TERMINADO!")
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"The script took {int(minutes)} minutes and {seconds:.0f} seconds to run.")

