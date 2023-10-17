from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd


class DataModelPreparation:
    def __init__(self, meses_testeo:int = 6, meses_prediccion:int = 6):
        self.meses_testeo = meses_testeo
        self.meses_prediccion = meses_prediccion
        self.data = self.load_data()
        self.train_df, self.test_df = self.train_test_separation()
        
    
    def load_data(self):
        df = pd.read_stata("./data/variables_productos_primarios.dta",index_col="fecha")
        df = df.drop(["mes","anio"],axis=1)
        df["pp"] = df.pp / 1_000_000
        df.index = df.index.to_period('M')
        return df
    
    def train_test_separation(self):
        train_df = self.data[:-self.meses_testeo].copy()
        test_df = self.data.copy()
        return train_df, test_df
        

