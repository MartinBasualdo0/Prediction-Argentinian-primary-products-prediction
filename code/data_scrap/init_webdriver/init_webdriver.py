from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
# from init_webdriver.download_folder import download_folder

def inicio_driver(link:str, download_folder:str):
    service = Service(ChromeDriverManager().install())
    # carpeta_descarga=os.getcwd().replace('src','downloads')
    carpeta_descarga=os.getcwd()+ download_folder
    # print(carpeta_descarga)
    prefs = {'download.default_directory' : carpeta_descarga,
        "directory_upgrade": True}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(link)
    driver.maximize_window()
    return driver
    
def every_downloads_chrome(download_folder:str):
    '''Check if all downloads are complete'''
    while True:
        carpeta_descarga=os.getcwd()+ download_folder
        time.sleep(.5)
        incomplete_downloads = [name for name in os.listdir(carpeta_descarga) if name.endswith('.tmp')]
        if not incomplete_downloads:
            return True  # Return True when no more .crdownload files in the directory
        time.sleep(1)  # Wait for 1 second before checking again


def wait_for_downloads_to_complete(download_folder:str, timeout:int = 100):
    '''Wait for all downloads to complete with a timeout'''
    start_time = time.time()  # Save the start time

    while not every_downloads_chrome(download_folder):  # Wait until all downloads are complete
        if time.time() - start_time > timeout:  # If the timeout has elapsed, break the loop
            print('Timeout elapsed, stopping downloads')
            break
        time.sleep(1)  # Wait for 1 second before checking again
    