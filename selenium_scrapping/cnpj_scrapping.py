import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_time_now():
    return pd.to_datetime('now', utc=True) - pd.to_timedelta('03:00:00')

def read_cnpjs(path):
    cnpjs = pd.read_csv(path)
    cnpjs['treated_cnpjs'] = cnpjs['CNPJs'].apply(lambda x: re.sub(r'\D', '', x))
    return cnpjs

def wdriver():
    options = Options()
    options.set_preference("network.cookie.cookieBehavior", 0)
    options.set_preference("dom.disable_open_during_load", False)
    options.set_preference("privacy.trackingprotection.enabled", False)
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    driver = webdriver.Firefox(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def open_page(driver, url):
    print('open_page')
    driver.maximize_window()
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    time.sleep(10)
    return driver

def find_captcha_box(driver):
    print('find captcha box')
    iframe = "//iframe[@title='Widget contendo caixa de seleção para desafio de segurança hCaptcha']"
    wait_captcha_button = WebDriverWait(driver, 30)
    captcha_iframe = wait_captcha_button.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe)))
    captcha_element = driver.find_element(By.ID, 'checkbox')
    return captcha_element

def wait_challenge_appears(driver):
    print('wait challenge appears')
    driver.switch_to.default_content()
    time.sleep(2)
    try:
        iframe_challenge = "//iframe[@title='Conteúdo principal do desafio hCaptcha']"
        wait_captcha_challenge = WebDriverWait(driver, 10)
        captcha_challenge_iframe = wait_captcha_challenge.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_challenge)))
        return captcha_challenge_iframe
    except Exception as e:
        print(f"Exception occurred while waiting for challenge to appear: {e}")

def wait_user_complete_challenge(driver):
    print('wait user complete challenge')
    try:
        iframe = "//iframe[@title='Conteúdo principal do desafio hCaptcha']"
        wait_captcha_challenge_gone = WebDriverWait(driver, 300)
        captcha_challenge_iframe_gone = wait_captcha_challenge_gone.until_not(EC.presence_of_element_located((By.XPATH, iframe)))
        time.sleep(20)
        driver.switch_to.default_content()
        return captcha_challenge_iframe_gone
    except Exception as e:
        print(f"Exception occurred while waiting for user to complete challenge: {e}")

def solve_captcha(driver):
    print('solve_captcha')
    captcha_box = find_captcha_box(driver)
    captcha_box.click()
    challenge_exists = wait_challenge_appears(driver)

    if challenge_exists:
        wait_user_complete_challenge(driver)

def captcha_was_done_right(driver):
    time.sleep(5)
    captcha_box = find_captcha_box(driver)
    check = captcha_box.get_attribute('aria-checked')
    driver.switch_to.default_content()
    return True if check == 'true' else False

def click_search(driver):
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

    search_button.click()
    print('click search')

def search_cnpj(driver, url_base, cnpj):
    # url = url_base + f'?cnpj={cnpj}'
    url = url_base + 'cnpjreva_solicitacao.asp?cnpj=16745465000101'
    driver = open_page(driver, url)
    solve_captcha(driver)

    if captcha_was_done_right(driver):
        click_search(driver)


    print('url mudou')

def collect_data(driver):
    ...

if __name__ == '__main__':
    path_cnpjs = 'input.csv'
    cnpjs = read_cnpjs(path_cnpjs)

    url_base = 'https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/'

    driver = wdriver()

    for cnpj in cnpjs['treated_cnpjs']:
        cnpj_infos = search_cnpj(driver, url_base, cnpj)

        collect_data(driver)
