import pytest
import pandas as pd
from bs4 import BeautifulSoup
from cnpj_pyautogui.read_html_file import (
    remove_unnamed_columns, remove_characters, load_html, parse_html,
    merge_secondary_activity, extract_fonts, clean_fonts,
    extract_data_from_fonts, create_dataframe, main, DONT_STORE
)

def test_remove_unnamed_columns():
    df = pd.DataFrame({
        'Unnamed: 0': [1, 2, 3],
        'Col1': [4, 5, 6],
        'Unnamed: 1': [7, 8, 9]
    })
    result = remove_unnamed_columns(df)
    expected_df = pd.DataFrame({'Col1': [4, 5, 6]})
    pd.testing.assert_frame_equal(result, expected_df)

def test_remove_characters():
    text = "\nHello\t World\n"
    result = remove_characters(text)
    assert result == "Hello World"

def test_load_html(tmp_path):
    content = "<html></html>"
    file_path = tmp_path / "test.html"
    file_path.write_text(content, encoding='iso-8859-1')

    result = load_html(file_path)
    assert result == content

def test_parse_html():
    content = "<html><body><p>Test</p></body></html>"
    soup = parse_html(content)
    assert soup.find('p').text == "Test"

def test_merge_secondary_activity():
    fonts = [
        "CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS",
        "Activity 1",
        "Activity 2",
        "CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA"
    ]
    result = merge_secondary_activity(fonts)
    expected = [
        "CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS",
        "Activity 1; Activity 2",
        "CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA"
    ]
    assert result == expected

def test_extract_fonts():
    content = "<html><body><table><tr><td><font>Test</font></td></tr></table></body></html>"
    soup = BeautifulSoup(content, 'html.parser')
    fonts = extract_fonts(soup)
    assert fonts[0].text == "Test"

def test_clean_fonts():
    fonts = [BeautifulSoup('<font>REPÚBLICA FEDERATIVA DO BRASIL</font>', 'html.parser').font,
             BeautifulSoup('<font>Sample Text</font>', 'html.parser').font]
    cleaned_fonts, removed_fonts = clean_fonts(fonts, DONT_STORE)
    assert cleaned_fonts[0].text == "Sample Text"
    assert removed_fonts[0].text == "REPÚBLICA FEDERATIVA DO BRASIL"

def test_extract_data_from_fonts():
    fonts = [
        BeautifulSoup('<font>Key1</font>', 'html.parser').font,
        BeautifulSoup('<font>Value1</font>', 'html.parser').font,
        BeautifulSoup('<font>Key2</font>', 'html.parser').font,
        BeautifulSoup('<font>Value2</font>', 'html.parser').font
    ]
    keys, values = extract_data_from_fonts(fonts)
    assert keys == ["Key1", "Key2"]
    assert values == ["Value1", "Value2"]

def test_create_dataframe():
    keys = ["Key1", "Key2"]
    values = ["Value1", "Value2"]
    df = create_dataframe(keys, values)
    expected_df = pd.DataFrame({"Key1": ["Value1"], "Key2": ["Value2"]})
    pd.testing.assert_frame_equal(df, expected_df)

# Test main
def test_main(tmp_path):
    content = """<html>
                 <body>
                   <table>
                     <tr><td><font>Key1</font></td></tr>
                     <tr><td><font>Value1</font></td></tr>
                     <tr><td><font>Key2</font></td></tr>
                     <tr><td><font>Value2</font></td></tr>
                   </table>
                 </body>
                 </html>"""
    file_path = tmp_path / "test.html"
    file_path.write_text(content, encoding='iso-8859-1')

    df = main(file_path, "12345678901234")
    expected_df = pd.DataFrame({
        "CNPJ": ["12345678901234"],
        "Key1": ["Value1"],
        "Key2": ["Value2"]
    })
    pd.testing.assert_frame_equal(df, expected_df)
