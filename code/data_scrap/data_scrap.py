# from init_webdriver.init_webdriver import inicio_driver, scrap_link_xls
from variables.excels_ica_digital import scrap_excels_ica_digital
from init_webdriver.download_folder import download_primary_products,download_pp_price_index
import os
import sys


if __name__ == "__main__":
    scrap_excels_ica_digital(xlsx_end_point="serie_rubros_usos_mensual.xlsx", download_folder=download_primary_products,timeout=10, replace=True)
    scrap_excels_ica_digital(xlsx_end_point="indices_expo.xlsx", download_folder=download_pp_price_index,timeout=10, replace=True)
    
