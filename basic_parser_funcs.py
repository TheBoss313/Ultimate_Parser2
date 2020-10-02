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
from pathlib import Path
logs.basicConfig(filename='ultimate.log', filemode='a', format='%(asctime)s %(levelname)s  %(message)s',
                 datefmt='%d-%b-%y %H:%M:%S', level=logs.INFO)


def get_html(url, name):
    r = requests.get(url)
    r.encoding = 'utf8'
    log_file('HTML Load Successful', name, link=url)
    return r.text


def get_file_ext(url):
    return url[url.rfind('.')+1:]


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
    message = f'{status} - {name} - {link}'
    if status != 'HTML Load Successful' or status != 'File Load Successful' or status.lower() != 'info':
        logs.critical(message)
    elif status.lower() == 'info':
        logs.info(message)
    else:
        logs.warning(message)


def get_images(links: list, folder_name, file_name, file_number: int = 0):
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/{folder_name}/{file_name}').mkdir(parents=True, exist_ok=True)
    for i in range(file_number, len(links)):
        urlb.urlretrieve(links[i],
                         f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/'
                         f'{folder_name}/{file_name}/{file_name}{i}.{get_file_ext(links[i])}')


def get_pdf(link: str, folder_name, file_name, file_number: int = 0):
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/{folder_name}/{file_name}').mkdir(parents=True, exist_ok=True)
    urlb.urlretrieve(link,
                     f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/{folder_name}/{file_name}/{file_name}{file_number}.pdf')


def ask_for_manual_url(name, tk):
    return sd.askstring("Manual Url", f"Url of {name}", parent=tk)
