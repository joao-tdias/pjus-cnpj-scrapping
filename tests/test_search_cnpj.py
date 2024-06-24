from selenium import webdriver
import pytest
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from cnpj_scrapping import open_page, solve_captcha, click_search, search_cnpj, wdriver, collect_data, get_time_now

def test_get_time_now():
    time_now = get_time_now()
    assert pd.Timestamp.now(tz='UTC').floor('min') - time_now.floor('min') == pd.to_timedelta('03:00:00')

def test_if_webdriver_was_created_right():
    driver = wdriver()
    assert isinstance(driver, webdriver.Chrome)
    driver.quit()

def test_if_driver_open_any_page():
    driver = wdriver()
    driver = open_page(driver, 'https://example.com')
    assert driver.current_url == 'https://example.com/'
    driver.quit()

def test_if_clicking_search_button_works_fine():
    driver = wdriver()
    open_page(driver, 'https://example.com')
    search_button = driver.execute_script("""
    var btn = document.createElement("button");
    btn.type = "submit";
    document.body.appendChild(btn);
    return btn;
    """)

    click_search(driver)
    driver.quit()

# def test_collect_data():
#     driver = wdriver()
#     open_page(driver, 'https://example.com')

#     driver.execute_script("""
#     var div = document.createElement("div");
#     div.id = "data";
#     div.innerText = "Test data";
#     document.body.appendChild(div);
#     """)

#     collect_data(driver)
#     # Verifique se os dados foram coletados corretamente
#     driver.quit()