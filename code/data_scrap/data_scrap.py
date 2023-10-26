# from init_webdriver.init_webdriver import inicio_driver, scrap_link_xls
from variables.excels_ica_digital import scrap_excels_ica_digital
from init_webdriver.download_folder import download_primary_products,download_pp_price_index, download_exchange_rates, download_inflation, download_precipitations
from variables.real_exchange_rate import get_exchange_rates
from variables.precipitations import request_precipitations
from variables.inflation import scrap_ipc
from alphacast_key import alphacast_key

def data_scrap():
    '''I should avoid to close and init the driver every time'''
    scrap_excels_ica_digital(xlsx_end_point="serie_rubros_usos_mensual.xlsx", download_folder=download_primary_products,timeout=10, replace=True)
    scrap_excels_ica_digital(xlsx_end_point="indices_expo.xlsx", download_folder=download_pp_price_index,timeout=10, replace=True)
    get_exchange_rates(download_exchange_rates)
    scrap_ipc(download_inflation, timeout=10, replace=True)
    request_precipitations(download_precipitations, alphacast_key)

if __name__ == "__main__":
    data_scrap()
