import pandas as pd
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ENCODING = 'iso-8859-1'
DONT_STORE = [
    'REPÚBLICA FEDERATIVA DO BRASIL',
    'CADASTRO NACIONAL DA PESSOA JURÍDICA',
    'COMPROVANTE DE INSCRIÇÃO E DE SITUAÇÃO CADASTRAL'
]

def remove_unnamed_columns(df):
    col_names = df.columns.tolist()
    new_col_names = [col for col in col_names if 'Unnamed' not in col]
    return df[new_col_names]

def remove_characters(text):
    return text.replace('\n', '').replace('\t', '').strip()

def load_html(file_path):
    try:
        with open(file_path, 'r', encoding=ENCODING) as file:
            content = file.read()
        return content
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo {file_path}: {e}")
        raise

def parse_html(content):
    try:
        return BeautifulSoup(content, 'html.parser')
    except Exception as e:
        logging.error("Erro ao parsear o conteúdo HTML: {e}")
        raise

def merge_secondary_activity(fonts):
    inicio = "CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS"
    fim = "CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA"
    nova_lista = []
    combinando = False
    combinacao = []

    for item in fonts:
        if item == inicio:
            combinando = True
            nova_lista.append(item)
        elif item == fim:
            if combinacao:
                nova_lista.append("; ".join(combinacao))
                combinacao = []
            combinando = False
            nova_lista.append(item)
        elif combinando:
            combinacao.append(item)
        else:
            nova_lista.append(item)

    return nova_lista

def extract_fonts(soup):
    try:
        table = soup.find('table')
        return table.find_all('font')
    except Exception as e:
        erro = soup.find_all('p')
        logging.error(f"Erro ao extrair fontes do HTML: {e}")
        return erro[1].text

def clean_fonts(fonts, dont_store):
    try:
        remove_list = []
        cleaned_fonts = []

        for font in fonts:
            text = remove_characters(font.text)
            if text not in dont_store:
                cleaned_fonts.append(font)
            else:
                remove_list.append(font)

        return cleaned_fonts, remove_list
    except Exception as e:
        logging.error(f"Erro ao limpar fontes: {e}")
        raise

def extract_data_from_fonts(fonts):
    secondary_activities = []
    new_list = [remove_characters(font.text) for font in fonts]
    new_list = merge_secondary_activity(new_list)

    try:
        keys = new_list[0::2]
        values = new_list[1::2]

        return keys, values
    except Exception as e:
        logging.error(f"Erro ao extrair dados das fontes: {e}")
        raise

def create_dataframe(keys, values):
    try:
        data_dict = {key: [] for key in keys}
        for key, value in zip(keys, values):
            data_dict[key].append(value)
        return pd.DataFrame(data_dict)
    except Exception as e:
        logging.error(f"Erro ao criar DataFrame: {e}")
        raise

def main(file_path, cnpj):
    try:
        content = load_html(file_path)
        soup = parse_html(content)
        fonts = extract_fonts(soup)
        if isinstance(fonts, str):
            df = pd.DataFrame()
            df['ERRO'] = [fonts]
        else:
            cleaned_fonts, _ = clean_fonts(fonts, DONT_STORE)
            keys, values = extract_data_from_fonts(cleaned_fonts)
            df = create_dataframe(keys, values)
        df.insert(0, 'CNPJ', cnpj)
        logging.info('Fim da limpeza')
        return df
    except Exception as e:
        logging.error(f"Erro no processamento principal: {e}")
        raise

if __name__ == "__main__":
    file_path = r'C:\Users\JoãoDias\Documents\ps\pjus-cnpj-scrapping\download_pages\17516113000147.htm'
    df = main(file_path, 17516113000147)
    print(df)
