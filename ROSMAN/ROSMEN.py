from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as ms
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import csv
from basic_parser_funcs import *
from ftp_parser_rosman import main_ftp
from URL_Validator import test_url

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


# Translits name for link
def translit_name(name: str):
    global eng, rus_l
    name = name.lower()
    name = name.replace(' ', '-')
    name = name.replace('...', '-')
    name = name.replace('.', '')
    name = name.replace(',', '')
    name = name.replace(':', '')
    end_name = ''
    for i in range(len(name)):
        if name[i] == '-':
            end_name = end_name + '-'
        elif name[i] in eng_l:
            end_name = end_name + name[i]
        elif name[i] in rus_l:
            a = rus_l.find(name[i])
            end_name = end_name + eng[a]
        elif name[i].isdigit():
            end_name = end_name + name[i]
    end_name = end_name.replace('--', '-')
    return end_name


# Writes the info into CSV file
def csv_read(data):
    with open("rosman_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['annotation']))


# Gets the info from soup
def get_head(html, name):
    if html == 404:
        return
    else:
        soup = BeautifulSoup(html, 'lxml')
        description = soup.find('div', class_='item-desc')
        if not description:
            description = soup.find('div', itemprop='description')
        description = description.get_text().replace('\n\n', '').replace('\t', '')
        data = {'annotation': description, 'name': name}
        csv_read(data)


def rosman(filename, button_info):
    y = 0
    names = []
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for line in lines:
        names.append(line.split(',', 1)[1])
    # Checks what is needed
    if button_info == 'textimg':
        for j in range(len(names)):
            name = names[j]
            link = f'https://www.rosman.ru/catalog/item/{translit_name(name)}/'
            print(f'{link} {y}')
            y += 1
            hatmail = get_html(link, name)
            main_ftp(lines)
            get_head(hatmail, name)
    elif button_info == 'text':
        for j in range(len(names)):
            name = names[j]
            link = f'https://www.rosman.ru/catalog/item/{translit_name(name)}/'
            print(f'{link} {y}')
            y += 1
            hatmail = get_html(link, name)
            get_head(hatmail, name)
    elif button_info == 'img':
        for j in range(len(names)):
            print(y)
            y += 1
            main_ftp(lines)
