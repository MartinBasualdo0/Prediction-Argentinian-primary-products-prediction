import pandas as pd
from alphacast import Alphacast

def request_precipitations(download_folder:str, alphacast_key:str) -> pd.DataFrame:
    alphacast = Alphacast(alphacast_key)
    precipitations = alphacast.datasets.dataset(37780).download_data("pandas")
    precipitations.to_excel("."+download_folder+"/precipitations.xlsx")
