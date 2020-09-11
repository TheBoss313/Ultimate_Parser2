from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import filedialog
import logging as logs
from tkinter import messagebox as ms
from pathlib import Path
logs.basicConfig(filename='ultimate.log', filemode='a', format='%(asctime)s %(levelname)s  %(message)s',
                 datefmt='%d-%b-%y %H:%M:%S', level=logs.DEBUG)


def get_html(url, name):
    r = requests.get(url)
    r.encoding = 'utf8'
    log_file('HTML Load Successful', name)
    return r.text


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
    message = f'{status}  {name}  {link}'
    if status != 'HTML Load Successful' or status != 'File Load Successful':
        logs.critical(message)
    elif status.lower() == 'debug':
        logs.debug(message)
    else:
        logs.info(message)
