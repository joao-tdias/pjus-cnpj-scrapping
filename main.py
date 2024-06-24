import pandas as pd
import logging
import re
from crawl_web import crawl_cnpj
from read_html_file import main, remove_unnamed_columns
import os
import sys

ROOT = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_FOLDER = os.path.join(ROOT, 'download_pages')

def read_cnpjs(path):
    try:
        cnpjs = pd.read_csv(path)
        cnpjs['treated_cnpjs'] = cnpjs['CNPJs'].apply(lambda x: re.sub(r'\D', '', x))
        return cnpjs
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {path}: {e}")
        raise

if __name__ == '__main__':
    path_input_cnpjs = 'input.csv'
    path_output_cnpjs = 'output.csv'
    cnpjs_to_search = read_cnpjs(path_input_cnpjs)
    for cnpj in cnpjs_to_search['treated_cnpjs']:
        output = pd.read_csv(path_output_cnpjs)
        if int(cnpj) not in list(output['CNPJ']):
            crawl_cnpj(cnpj)
            df = main(os.path.join(DOWNLOAD_FOLDER, cnpj+'.htm'), cnpj)
            new_df = pd.concat([output, df], ignore_index=True)
            new_df = remove_unnamed_columns(new_df)
            new_df.to_csv('output.csv')
        else:
            print('CNPJ já coletado', cnpj)

