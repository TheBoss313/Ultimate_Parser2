from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as ms
import urllib.request as urlb
import urllib as urlb1
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import csv
from text_cleanup import *


def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text


def get_dt(html, name):
    soup = BeautifulSoup(html, 'lxml')
    a = soup.findAll('table')[1].findAll('tr')
    insides = []
    title = ''
    pages = 0
    size = ''
    cover = ''
    isbn = ''
    description = ''
    for tr in range(len(a)):
        b = a[tr].findAll('td')
        for td in range(len(b)):
            if tr == 0 and td == 0:
                for d in b[td].find_all('a', href=True):
                    insides.append(d['href'])
            elif tr == 0 and td == 1:
                for d in b[td].find_all('h1'):
                    title = d.text.strip()
                e = b[td].find('div', class_='left').text.strip()
                e = e.replace('  ', '').replace('\t', '')
                ee = e.split('\n')
                for eee in ee:
                    if 'Объем: ' in eee:
                        pages = (eee[eee.find('Объем: ') + len('Объем: '):])
                    elif 'Формат: ' in eee:
                        size = (eee[eee.find('Формат: ') + len('Формат: '):])
                    elif 'Тип переплета: ' in eee:
                        cover = (eee[eee.find('Тип переплета: ') + len('Тип переплета: '):])
                    elif 'ISBN: ' in eee:
                        isbn = (eee[eee.find('ISBN: ') + len('ISBN: '):])
                    else:
                        pass
            elif tr == 1 and td == 0:
                for d in b[td].find_all('img'):
                    insides.append(d.get('src'))
            elif tr == 1 and td == 1:
                description = b[td].text.strip()
                description = empty_lines(description)
    data = {'title': title, 'pages': pages, 'cover': cover, 'size': size, 'isbn': isbn, 'desc': description}
    for i in range(len(insides)):
        Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/rech/{name}').mkdir(parents=True, exist_ok=True)
        urlb.urlretrieve(f'http://www.rech-deti.ru/{insides[i]}', f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser'
                                                                  f'/images/rech/{name}/{i}.jpg')
