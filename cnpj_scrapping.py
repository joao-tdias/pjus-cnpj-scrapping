import pandas as pd
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
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
    ...
def collect_data(driver):
    ...
if __name__ == '__main__':
    path_cnpjs = 'input.csv'
    cnpjs = pd.read_csv(path_cnpjs)    url_base = 'https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp'
    cnpjs = read_cnpjs(path_cnpjs)

    url_base = 'https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp'

    driver = wdriver()
    for cnpj in cnpjs['treated_cnpjs']:
        cnpj_infos = search_cnpj(driver, url_base, cnpj)

        collect_data(driver)
