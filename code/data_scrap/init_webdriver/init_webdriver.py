from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

def inicio_driver(link:str, downloads_folder:str):
    service = Service(ChromeDriverManager().install())
    # carpeta_descarga=os.getcwd().replace('src','downloads')
    carpeta_descarga=os.getcwd()+'\\downloads'
    print(carpeta_descarga)
    # prefs = {'download.default_directory' : carpeta_descarga,
    #     "directory_upgrade": True}
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.get(link)
    # driver.maximize_window()
    # return driver


def every_downloads_chrome(driver):
    '''Para ver cuando terminan las descargas'''
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
    
def scrap_link_xls(url:str):
    driver = inicio_driver(url)
    # waits for all the files to be completed and returns the paths
    paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
    