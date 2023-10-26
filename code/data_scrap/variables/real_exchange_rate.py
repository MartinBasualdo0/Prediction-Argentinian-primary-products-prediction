import yfinance as yf
import pandas as pd

def get_exchange_rates(download_folder:str) -> pd.DataFrame:
    acciones = [
        ('GGAL', 'GGAL.BA', 10),
        ('YPF', 'YPFD.BA', 1),
        ('PAM', 'PAMP.BA', 25),
    ]

    adrs = pd.DataFrame()
    locales = pd.DataFrame()
    ccls = pd.DataFrame()

    for accion in acciones:
        tmp_adr = yf.download(accion[0], period='1d' , start=2004)['Adj Close']
        tmp_adr.index = tmp_adr.index.tz_localize(None).round("D")
        adrs[accion[0]] = tmp_adr
        tmp_loc = yf.download(accion[1], period='1d' , start=2004)['Adj Close']
        tmp_loc.index = tmp_loc.index.tz_localize(None).round("D")
        locales[accion[1]] = tmp_loc

        ccls[accion[0]] = locales[accion[1]] * accion[2] / adrs[accion[0]]
        ccls[accion[0]].interpolate(method='linear',inplace=True)

    ars = yf.download("ARS=X", period='1d' , start=2004)['Adj Close']
    ars.index = ars.index.tz_localize(None).round("D")
    ars_mensual = ars.resample("M").mean()

    ccl = ccls.mean(axis=1)
    ccl_mensual = ccl.resample("M").mean()
    brecha_bruta = (ccl/ars).ffill().fillna(1)
    brecha_neta = brecha_bruta - 1
    brecha_neta_mensual = brecha_neta.resample("M").mean()
    brecha_bruta_mensual = 1+brecha_neta_mensual

    df = pd.concat([ccl_mensual, ars_mensual, brecha_bruta_mensual],axis=1)
    df.columns = ["dolar_ccl","offic_er","gap"]
    # print("."+download_folder)
    df.to_excel("."+download_folder+"/exchange_rates.xlsx")
    return df




