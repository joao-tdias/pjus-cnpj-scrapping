import pyautogui
import pandas as pd
import re
from time import sleep
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL_BASE = 'https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp'
SLEEP_SHORT = 0.5
SLEEP_MEDIUM = 0.5
SLEEP_LONG = 1

positions = {
    'url': pyautogui.Point(x=4748, y=81),
    'captcha_check': pyautogui.Point(x=5086, y=638),
    'input_cnpj': pyautogui.Point(x=4239, y=660),
    'consultar': pyautogui.Point(x=4168, y=764),
    'save_as_right_click': pyautogui.Point(x=4986, y=885),
    'save_as_select': pyautogui.Point(x=5066, y=954),
    'save_button': pyautogui.Point(x=5298, y=629),
    'rename_file': pyautogui.Point(x=4941, y=545)
}

def access_new_url(url):
    try:
        pyautogui.click(positions['url'])
        sleep(SLEEP_MEDIUM)
        pyautogui.hotkey('ctrl', 'a')
        sleep(SLEEP_SHORT)
        pyautogui.press('backspace')
        pyautogui.write(url)
        sleep(SLEEP_SHORT)
        pyautogui.press('enter')
    except Exception as e:
        logging.error(f"Erro ao acessar a URL {url}: {e}")
        raise

def insert_cnpj(cnpj):
    try:
        sleep(SLEEP_LONG)
        pyautogui.click(positions['input_cnpj'])
        sleep(SLEEP_MEDIUM)
        pyautogui.write(cnpj, interval=0.1)
    except Exception as e:
        logging.error(f"Erro ao inserir o CNPJ {cnpj}: {e}")
        raise

def captcha():
    try:
        pyautogui.click(positions['captcha_check'])
        logging.info('Esperando o usuário finalizar o CAPTCHA')
        sleep(8)
    except Exception as e:
        logging.error(f"Erro ao clicar no CAPTCHA: {e}")
        raise

def search():
    try:
        sleep(SLEEP_MEDIUM)
        pyautogui.click(positions['consultar'])
    except Exception as e:
        logging.error(f"Erro ao clicar no botão de consultar: {e}")
        raise

def rename_file(cnpj):
    try:
        pyautogui.click(positions['rename_file'])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(cnpj)
    except Exception as e:
        logging.error(f"Erro ao renomear o arquivo para {cnpj}: {e}")
        raise

def save_html(cnpj):
    try:
        sleep(SLEEP_LONG)
        pyautogui.click(positions['save_as_right_click'], button='right')
        sleep(SLEEP_SHORT)
        pyautogui.click(positions['save_as_select'], button='left')
        sleep(SLEEP_MEDIUM)
        rename_file(cnpj)
        pyautogui.click(positions['save_button'])
        sleep(SLEEP_LONG)
    except Exception as e:
        logging.error(f"Erro ao salvar a página HTML para {cnpj}: {e}")
        raise

def crawl_cnpj(cnpj):
    """Realiza o crawl de todos os CNPJs fornecidos."""
    logging.info(f"Iniciando processamento do CNPJ: {cnpj}")
    access_new_url(URL_BASE)
    insert_cnpj(cnpj)
    captcha()
    search()
    save_html(cnpj)
    logging.info(f"Processamento do CNPJ {cnpj} concluído")

if __name__ == '__main__':
    cnpj = '17516113000147'
    crawl_cnpj(cnpj)
