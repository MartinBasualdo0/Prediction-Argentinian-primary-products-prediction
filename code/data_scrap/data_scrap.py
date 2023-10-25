# from init_webdriver.init_webdriver import inicio_driver, scrap_link_xls
from variables.productos_primarios import scrap_excels_expo_ica_digital
import os
import sys


if __name__ == "__main__":
    scrap_excels_expo_ica_digital(timeout=10, replace=True)