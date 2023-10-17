import pandas as pd
from sarima_model_preparation import DataModelPreparation
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error as mean_squared_error
import time
import numpy as np
import math

start_time = time.time()
max_p = 9
max_q = 9
Data = DataModelPreparation(meses_prediccion=6, meses_testeo=6)
variable = "pp"
existe_estacionalidad = True
transform_log = False
X = Data.train_df[["itcr", "ip", "pre"]]


def agrega_fila_datos_modelo(calibration_df: pd.DataFrame, variable: str, existe_estacionalidad:bool, transform_log:bool,p:int,d:int,q:int,
                             P:int=None, D:int=None, Q:int=None, M:int=None):
    seasonal_order = (P,D,Q,M) if existe_estacionalidad else (0,0,0,0)  # provide a default value
    y = np.log(Data.train_df[variable] + 1) if transform_log else Data.train_df[variable]
    sarima_exog = SARIMAX(y, order = (p,d,q),exog=X, seasonal_order=seasonal_order)
    try:
        model_fit = sarima_exog.fit(maxiter=20_000)
        fitted_values = np.exp(model_fit.fittedvalues) if transform_log else model_fit.fittedvalues
        aic = model_fit.aic
        MSE = mean_squared_error(fitted_values, Data.train_df[variable])
        RMSE = math.sqrt(MSE)
    except Exception as e:
        print(f"Failed to fit model {p,d,q,Q,D,Q,M} for variable {variable}. Error: {e}")
        aic = "error"
        MSE = "error"
        RMSE = "error"
    new_row = {
        'variable': variable,
        'p': p,
        'd': d,
        'q': q,
        'P': P,
        'D': D,
        'Q': Q,
        'M': M,
        'AIC': aic,
        'MSE': MSE,
        'RMSE':RMSE
    }
    calibration_df.loc[len(calibration_df)] = new_row
    
calibration_df = pd.DataFrame(columns=['variable', 'p', 'd', 'q', 'P', 'D', 'Q', 'M', 'AIC', 'MSE','RMSE'])
for p in range(0,max_p+1):
    for d in range(0,2):
        for q in range(0,max_q+1):
            if existe_estacionalidad:   
                for P in range(0,2):
                    for D in range(0,2):
                        for Q in range(0,2):
                            M=12
                            print("MODELO!!!",p,d,q,P,D,Q,M)
                            agrega_fila_datos_modelo(calibration_df, variable, existe_estacionalidad, transform_log, 
                                                     p,d,q,
                                                     P=P,D=D,Q=Q,M=M)
            else:
                agrega_fila_datos_modelo(calibration_df, variable, existe_estacionalidad, transform_log,p,d,q)
                
calibration_df = calibration_df.drop_duplicates()  
calibration_df.to_excel(f"./data/calibration/calibration_{variable}.xlsx", index=False)

end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)
print(f"The script took {int(minutes)} minutes and {seconds:.0f} seconds to run.")