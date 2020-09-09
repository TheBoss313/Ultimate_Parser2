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


data = '''
<td class="cover" valign="top">
<a href="/upload/iblock/ea7/ea72966465cde6ae6674321dcd95d1af.jpg" rel="lightbox"><img alt="Пьесы" src="/upload/iblock/ea7/ea72966465cde6ae6674321dcd95d1af.jpg" title="Пьесы"/></a>
</td>
'''


def get_dt(html):
    soup = BeautifulSoup(html, 'lxml')
    a = soup.findAll('table')[1].findAll('tr')
    for tr in range(len(a)):
        b = a[tr].findAll('td')
        for td in range(len(b)):
            if tr == 0 and td == 0:
                for d in b[td].find_all('a', href=True):
                    front_page = d['href']
            # TODO ADD INFO PARSING
            elif tr == 0 and td == 1:
                print(b[td])
                for d in b[td].find_all('h1'):
                    title = d.text.strip()
            elif tr == 1 and td == 0:
                images = []
                for d in b[td].find_all('img'):
                    images.append(d.get('src'))
            elif tr == 1 and td == 1:
                description = b[td].text.strip()
                description = empty_lines(description)


def get_dt2(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup['href'])


def get_dt3(html):
    soup = BeautifulSoup(html, 'lxml')
    for a in soup.find_all('a', href=True):
        print(a['href'])


link = 'http://www.rech-deti.ru/catalog/7/61021/'
get_dt(get_html(link))
