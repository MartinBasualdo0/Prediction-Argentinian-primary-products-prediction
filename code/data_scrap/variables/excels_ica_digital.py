from init_webdriver.init_webdriver import inicio_driver, every_downloads_chrome
from init_webdriver.download_folder import download_primary_products
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from glob import glob
import os

def get_ica_digital_href(driver, timeout:int = 10):
    wait = WebDriverWait(driver, timeout)

    # Define the expected condition to wait for
    expected_condition = EC.presence_of_all_elements_located((By.XPATH, "//a[@class='btn btn-outline-success w-100 btn-sm max-w']"))

    # Wait for the elements to be loaded
    href_elements = wait.until(expected_condition)

    elements = driver.find_elements(By.XPATH, "//a[@class='btn btn-outline-success w-100 btn-sm max-w']")
    hrefs = [element.get_attribute('href') for element in elements]
    link_ica_digital = [href for href in hrefs if "ica_digital" in href][0]
    return link_ica_digital


def scrap_excels_ica_digital(xlsx_end_point:str,download_folder:str, timeout:int = 10, replace:bool = True):
    if replace:
        download_rute = "."+download_folder+"\*"
        for file in glob(download_rute, recursive = True): os.remove(file)
    driver = inicio_driver("https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-2-40", download_folder=download_folder)
    link_ica_digital = get_ica_digital_href(driver,timeout)
    driver.get(link_ica_digital+f"data/cuadros/{xlsx_end_point}")
    paths = WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
    driver.quit()