import pandas as pd
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
def wdriver():
    options = Options()
    # options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    return driver

if __name__ == '__main__':
    path_cnpjs = 'input.csv'
    cnpjs = pd.read_csv(path_cnpjs)    url_base = 'https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp'
    driver = wdriver()
