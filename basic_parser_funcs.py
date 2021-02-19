import webbrowser
from tkinter import simpledialog as sd
import requests
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as ms
from URL_Validator import *
import logging as logs
from bs4 import BeautifulSoup
import urllib.request as urlb
import urllib
import requests
import unicodedata
from pathlib import Path

logs.basicConfig(filename='ultimate.log', filemode='a', format='%(asctime)s %(levelname)s  %(message)s',
                 datefmt='%d-%b-%y %H:%M:%S', level=logs.CRITICAL)
rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
       'f', 'h', 'ts', 'ch', 'sh', 'shh', '', 'y', '', 'e', 'yu', 'ya']


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C").replace(' ', '-')


# Translits name for link
def translit_name2(name: str, english: list):
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
    end_name = end_name.replace('--', '-')
    return end_name


def get_html(url, name):
    r = requests.get(url)
    r.encoding = 'utf8'
    log_file('HTML Load Successful', name, link=url)
    return r.text


def get_file_ext(url):
    return url[url.rfind('.') + 1:]


def Loadfile():
    tk = Tk()
    filename = filedialog.Open(tk, filetypes=[('*.txt files', '.txt')]).show()
    if filename == '':
        return
    tk.destroy()
    log_file('File Load Successful', Path(filename).name)
    return filename


def log_file(status, name, **kwargs):
    link = kwargs.get('link', None)
    name = translit_name2(name, eng)
    message = f'{status} - {name} - {link}'
    if status == '2ERROR 404':
        logs.critical(message)
    elif status != 'HTML Load Successful' or status != 'File Load Successful' or status.lower() != 'info':
        logs.error(message)
    elif status.lower() == 'info':
        logs.info(message)

    else:
        logs.warning(message)


def get_images(links: list, folder_name, file_name, file_number: int = 0, file_ext=''):
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/{folder_name}/{file_name}').mkdir(parents=True,
                                                                                                  exist_ok=True)
    for i in range(file_number, len(links)):
        if file_ext == '':
            file_ext = get_file_ext(links[i])
        file_name = remove_control_characters(file_name)
        link = remove_control_characters(links[i])
        try:
            urlb.urlretrieve(link,
                             f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/'
                             f'{folder_name}/{file_name}/{file_name}{i}.{file_ext}')
        except urllib.error.HTTPError:
            r = requests.get(link)
            with open(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/'
                      f'{folder_name}/{file_name}/{file_name}{i}.{file_ext}', 'wb') as outfile:
                outfile.write(r.content)


def get_pdf(link: str, folder_name, file_name, file_number: int = 0):
    link = remove_control_characters(link)
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/{folder_name}/{file_name}').mkdir(parents=True,
                                                                                                  exist_ok=True)
    try:
        urlb.urlretrieve(link,
                         f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/{folder_name}/'
                         f'{file_name}/{file_name}{file_number}.pdf')
    except urllib.error.HTTPError:
        r = requests.get(link)
        with open(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/'
                  f'{folder_name}/{file_name}/{file_name}{file_number}.pdf', 'wb') as outfile:
            outfile.write(r.content)


def ask_for_manual_url(name, tk):
    return sd.askstring("Manual Url", f"Url of {name}", parent=tk)
