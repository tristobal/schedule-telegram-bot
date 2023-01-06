import datetime as dt
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from util.constants import ON_RENDER

AREA_COMBOBOX_ID = 'xxx'
AREA_DERMATOLOGY_ID = '5'
SPECIALITY_COMBOBOX_ID = 'zzz'
SPECIALITY_GENERAL_DERMATOLOGY_ID = '115'
SEARCH_BUTTON_ID = 'dnn_ctr10551_WCitawebmovil_imbBuscar'
DOCTORS_TABLE_ID = 'dnn_ctr10551_WCitawebmovil_GridView1'
URL = 'https://www.redclinica.cl/institucional/citas-web-presencial.aspx?id=1'


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_driver():
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    print(f'{now()} ON_RENDER: {ON_RENDER}')
    if ON_RENDER:
        return webdriver.Chrome(options=chrome_options)
    else:
        chromedriver_path = os.path.abspath('../chromedriver')
        chrome_service = Service(chromedriver_path)
        return webdriver.Chrome(service=chrome_service, options=chrome_options)


def search_schedule():
    response = ""
    driver = get_driver()
    print(f'{now()} Visiting: {URL}')
    driver.get(URL)

    print(f'{now()} {driver.title}')

    select_area = Select(driver.find_element(By.ID, AREA_COMBOBOX_ID))
    select_area.select_by_value(AREA_DERMATOLOGY_ID)
    driver.implicitly_wait(1)

    select_speciality = Select(driver.find_element(By.ID, SPECIALITY_COMBOBOX_ID))
    select_speciality.select_by_value(SPECIALITY_GENERAL_DERMATOLOGY_ID)

    driver.find_element(By.ID, SEARCH_BUTTON_ID).click()
    table_id = driver.find_element(By.ID, DOCTORS_TABLE_ID)
    rows = table_id.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        col = row.find_elements(By.TAG_NAME, "td")
        if col and "BERTUCCI" in col[1].text:
            button_ = col[5]
            input_ = button_.find_element(By.TAG_NAME, "input")
            response = f'{col[1].text}: {input_.get_attribute("value")}'

    driver.quit()
    return response
