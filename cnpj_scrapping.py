import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_time_now():
    return pd.to_datetime('now', utc=True) - pd.to_timedelta('03:00:00')

def read_cnpjs(path):
    cnpjs = pd.read_csv(path)
    cnpjs['treated_cnpjs'] = cnpjs['CNPJs'].apply(lambda x: re.sub(r'\D', '', x))
    return cnpjs

def wdriver():
    options = Options()
    # options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    return driver

def search_cnpj(driver, url_base, cnpj):
    url = url_base + f'?cnpj={cnpj}'
    driver.maximize_window()
    driver.get(url)
    wait_captcha_button = WebDriverWait(driver, 10)
    captcha_iframe = wait_captcha_button.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))
    captcha_element = driver.find_element(By.ID, 'checkbox')
    captcha_element.click()

    driver.switch_to.default_content()
    wait_captcha_challenge = WebDriverWait(driver, 10)
    captcha_challenge_iframe = wait_captcha_challenge.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='Conteúdo principal do desafio hCaptcha']")))

    wait_captcha_challenge_gone = WebDriverWait(driver, 300)
    captcha_challenge_iframe = wait_captcha_challenge_gone.until_not(EC.presence_of_element_located((By.XPATH, "//iframe[@title='Conteúdo principal do desafio hCaptcha']")))

    driver.switch_to.default_content()
    search_button  = driver.find_element(By.XPATH, "//button[@type='submit']")

    search_button.click()

    wait_captcha_button.until(
        EC.url_changes(driver.current_url)
    )
    ...



def collect_data(driver):
    ...



if __name__ == '__main__':
    path_cnpjs = 'input.csv'
    cnpjs = read_cnpjs(path_cnpjs)

    url_base = 'https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp'

    driver = wdriver()

    for cnpj in cnpjs['treated_cnpjs']:
        cnpj_infos = search_cnpj(driver, url_base, cnpj)

        collect_data(driver)
