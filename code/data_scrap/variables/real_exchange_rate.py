import yfinance as yf
import pandas as pd

def get_exchange_rates(download_folder:str) -> pd.DataFrame:
    shares = [
        ('GGAL', 'GGAL.BA', 10),
        ('YPF', 'YPFD.BA', 1),
        ('PAM', 'PAMP.BA', 25),
    ]

    adrs = pd.DataFrame()
    locales = pd.DataFrame()
    ccls = pd.DataFrame()

    for share in shares:
        tmp_adr = yf.download(share[0], period='1d' , start=2004)['Adj Close']
        tmp_adr.index = tmp_adr.index.tz_localize(None).round("D")
        adrs[share[0]] = tmp_adr
        tmp_loc = yf.download(share[1], period='1d' , start=2004)['Adj Close']
        tmp_loc.index = tmp_loc.index.tz_localize(None).round("D")
        locales[share[1]] = tmp_loc

        ccls[share[0]] = locales[share[1]] * share[2] / adrs[share[0]]
        ccls[share[0]].interpolate(method='linear',inplace=True)

    ars = yf.download("ARS=X", period='1d' , start=2004)['Adj Close']
    ars.index = ars.index.tz_localize(None).round("D")
    ars_monthly = ars.resample("M").mean()

    ccl = ccls.mean(axis=1)
    ccl_monthly = ccl.resample("M").mean()
    gross_gap = (ccl/ars).ffill().fillna(1)
    net_gap = gross_gap - 1
    net_gap_monthly = net_gap.resample("M").mean()
    gross_gap_monthly = 1+net_gap_monthly

    df = pd.concat([ccl_monthly, ars_monthly, gross_gap_monthly],axis=1)
    df.columns = ["dolar_ccl","offic_er","gap"]
    df.to_excel("."+download_folder+"/exchange_rates.xlsx")
    return df




