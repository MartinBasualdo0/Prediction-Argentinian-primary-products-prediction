import pandas as pd
from glob import glob

def read_primary_products():
    df = pd.read_excel("./code/data_scrap/downloads/primary_products/serie_rubros_usos_mensual.xlsx",
                       dtype=dict(año = "str",mes="str"))
    df = df.query('rubro_uso == "Productos primarios (PP)"')
    df.index = pd.to_datetime(df.mes + "-"+ df.año, format="%m-%Y")
    df = df[["valor"]]
    df = df.resample('M').mean()
    df = df.rename({"valor":"pp"},axis=1)
    return df

def read_pp_price_index():
    df = pd.read_excel("./code/data_scrap/downloads/pp_price_index/indices_expo.xlsx",
                       dtype=dict(Año = "str",Mes="str")
                       )
    df.index = pd.to_datetime(df.Mes + "-"+ df.Año, format="%m-%Y")
    df = df[['índice de precios de los productos primarios']]
    df = df.resample('M').mean()
    df = df.rename({"índice de precios de los productos primarios": "primary_products_price_index"},axis=1)
    return df

def read_inflation():
    ipc_indec=(pd.read_excel(glob('code/data_scrap/downloads/exchange_rate/inflation/sh_ipc*')[0],skipfooter=5,header=5,sheet_name=2)
        .T.reset_index()
        .rename({'index':'period',3:'inflation'},axis=1))[['period','inflation']][1:].reset_index(drop=True)
    ipc_indec.period=pd.to_datetime(ipc_indec.period).apply(lambda x: x.strftime('%d/%m/%Y'))

    ipc_geres=(pd.read_excel('code/data_scrap/downloads/exchange_rate/gerez_inflation/inflacion nivel general_ GERES.xlsx',header=2)
    .rename({'NIVEL (dic 2001=100)':'inflation', "Período":"period"},axis=1))[['period','inflation']]
    ipc_geres.period=pd.to_datetime(ipc_geres.period).apply(lambda x: x.strftime('%d/%m/%Y'))
    #Cambio de base a 2001
    coef=ipc_geres[ipc_geres.period=='01/12/2016'].inflation.values[0]/ipc_indec.inflation[0]
    ipc_indec.inflation=ipc_indec.inflation*coef

    ipc_gral = pd.concat([ipc_geres,ipc_indec])
    ipc_gral.period = pd.to_datetime(ipc_gral.period, format="%d/%m/%Y")
    ipc_gral = ipc_gral.set_index("period")
    ipc_gral = ipc_gral.resample('M').mean()
    return ipc_gral

def read_exchange_rate():
    df = pd.read_excel("code\data_scrap\downloads\exchange_rate\exchange_rates.xlsx", index_col="Date")
    return df

def read_precipitations():
    df = pd.read_excel("code\data_scrap\downloads\precipitations\precipitations.xlsx")
    df.Date = pd.to_datetime(df.Date, format="%Y-%m-%d")
    df["month"] = df.Date.dt.month
    df["year"] = df.Date.dt.year
    stations = ["ROSARIO","JUNIN", "MARCOS JUAREZ"]
    df = df.query("Station_name in @stations")
    df = df.groupby([df.month, df.year],as_index=False).agg({"Precipitations":"mean"})
    df.index = pd.to_datetime(df.year.astype(str) + "-" + df.month.astype(str), format="%Y-%m")
    df = df[["Precipitations"]].rename({"Precipitations":"precipitations"},axis=1)
    df = df.resample('M').mean()
    return df

def get_real_exchange_rate():
    inflation = read_inflation()
    exchange_rate = read_exchange_rate()
    df = exchange_rate.merge(inflation, left_index=True,right_index=True, how="inner")
    df["exchange_rate_today_prices"]  = df["offic_er"] * (df["inflation"].iloc[-1] / df["inflation"])
    df = df[["gap", "exchange_rate_today_prices"]]
    df = df.rename({"gap":"exchange_rate_gap"},axis=1)
    return df

def data_creation():
    primary_products = read_primary_products()
    primary_products_price_index = read_pp_price_index()
    exchange_rate_data = get_real_exchange_rate()
    precipitations = read_precipitations()
    df = primary_products.merge(primary_products_price_index, right_index=True, left_index=True, how="inner")
    df = df.merge(exchange_rate_data, right_index=True, left_index=True, how="inner")
    df = df.merge(precipitations, right_index=True, left_index=True, how="inner")
    df.to_excel("data/data.xlsx") 
    return df

if __name__ == "__main__":
    data_creation()