import pandas as pd
import os
from init_webdriver.init_webdriver import inicio_driver, wait_for_downloads_to_complete
from glob import glob #para eliminar archivos dentro de carpeta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def get_ipc_href(driver, timeout:int = 10):
    xls_div = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-color2')))
    hrefs=[]
    for element in xls_div:
        elemento=element.get_attribute('href')
        if elemento != None:
            hrefs.append(elemento)
    ip_indec = hrefs[0]
    return ip_indec
    
    
    
def scrap_ipc(download_folder:str, timeout:int = 10, replace:bool = True):
    if replace:
        download_rute = "."+download_folder+"\*"
        for file in glob(download_rute, recursive = True): os.remove(file)
    driver = inicio_driver("https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31", download_folder=download_folder)
    link_ipc_indec = get_ipc_href(driver,timeout)
    driver.get(link_ipc_indec)
    # paths = WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
    wait_for_downloads_to_complete(download_folder)
    driver.quit()