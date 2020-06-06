import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
#рейтинг аппаратов с ценами, + и -:)
URL = 'https://www.expertcen.ru/article/ratings/luchshie-zerkalnye-fotoapparati.html'
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
photorate = soup.find_all('td', class_ = 'ar-cit-1')
#Паттерн
pattern1 = r'(?:\d{2,3}\s\d{3})'
pattern2 = r'(?<=\A\n{6}).*'
pattern3 = r'(?<=Основные плюсы:\n{1}\s{52}\n).*'
pattern4 = r'(?<=Минусы:\n).*'
model_list = [] # список моделей
price_list = [] # список цен
plus_list = [] # список плюсов
minus_list = [] # список минусов
dict_info = dict.fromkeys(['Модель', 'Цена', 'Плюсы', 'Минусы']) # создаем словарь для сбора информации
for rev in photorate:
    text_str = str(rev.text)
    text_str.strip()                      # алгоритм
    price_info = re.findall(pattern1, text_str)
    price_str = str(price_info)
    price_str = price_str[2:(len(price_str) - 2)]
    price_list.append(price_str)
    model_info = re.findall(pattern2, text_str)
    model_str = str(model_info)
    model_str = model_str[2:(len(model_str) - 2)]
    model_list.append(model_str)
    plus_info = re.findall(pattern3, text_str)
    plus_str = str(plus_info)
    plus_str = plus_str[2:(len(plus_str) - 3)]
    plus_list.append(plus_str)
    minus_info = re.findall(pattern4, text_str)
    minus_str = str(minus_info)
    minus_str = minus_str[2:(len(minus_str) - 3)]
    minus_list.append(minus_str)
# заполняем словарь
dict_info['Модель'] = model_list
dict_info['Цена'] = price_list
dict_info['Плюсы'] = plus_list
dict_info['Минусы'] = minus_list
#pandas, формируем DataFrame
infoDF = pd.DataFrame(dict_info)
infoDF.to_csv('infoDF.csv') # создаем csv
# считаем csv
DataFrame_from_csv = pd.read_csv('infoDF.csv')
print(DataFrame_from_csv)
