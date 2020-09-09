from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as ms
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import csv

from ftp_parser_rosman import main_ftp
from URL_Validator import test_url
t = Tk()
t.title('ROSMEN Parser')
t.resizable(False, False)
filename_name = ''
filename = Label(t, text='NO FILE SELECTED')
y = 1
names = []
lines = []
text = IntVar()
img = IntVar()
rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


def log_write(status, name, **kwargs):
    """
    Function that creates a log file
    :param status: What Happened
    :param name: Book Name
    :param code: book AST or ASE code
    :param kwargs: link
    :return: ads the event into a log file
    """
    link = kwargs.get('link', None)
    with open('rosmen.csv', 'a', encoding='utf8') as logs:
        log = csv.writer(logs)
        if link != '':
            log.writerow((status, name))
        else:
            log.writerow((status, name, link))
    logs.close()


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


# Loads file
def Loadfile():
    global isbns, filename, filename_name
    filename1 = filedialog.Open(t, filetypes=[('*.txt files', '.txt')]).show()
    if filename1 == '':
        return
    filename2 = Path(filename1)
    filename.config(text=filename2.name)
    filename_name = filename1
    log_write('File Load Successful', filename2.name)


# Writes the info into CSV file
def csv_read(data):
    with open("rosman_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['annotation']))


# Gets the HTML from URL
def get_html(url, name):
    test = test_url(url)
    if test != 'Good':
        log_write(test, name, link=url)
        print(test)
        return 404
    else:
        r = requests.get(url)
        r.encoding = 'utf8'
        log_write('Html Loading Successful', name, link=url)
        return r.text


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


# Returns textimg text img depending on checked CheckButtons
def get_button_info():
    global text, img
    strong = ''
    if text.get() == 1:
        strong = strong + 'text'
    if img.get() == 1:
        strong = strong + 'img'
    if strong == '':
        ms.showerror('NO OPTION SELECTED', 'PLEASE SELECT TEXT, IMAGES OR BOTH!')
        return 'ERROR'
    return strong


def main():
    global y, names, lines
    # Gets info from file
    with open(filename_name, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for line in lines:
        names.append(line.split(',', 1)[1])
    # Checks what is needed
    if get_button_info() == 'textimg':
        for j in range(len(names)):
            name = names[j]
            link = f'https://www.rosman.ru/catalog/item/{translit_name(name)}/'
            print(f'{link} {y}')
            y += 1
            hatmail = get_html(link, name)
            main_ftp(lines)
            get_head(hatmail, name)
    elif get_button_info() == 'text':
        for j in range(len(names)):
            name = names[j]
            link = f'https://www.rosman.ru/catalog/item/{translit_name(name)}/'
            print(f'{link} {y}')
            y += 1
            hatmail = get_html(link, name)
            get_head(hatmail, name)
    elif get_button_info() == 'img':
        for j in range(len(names)):
            print(y)
            y += 1
            main_ftp(lines)
    lines = []
    names = []
    y = 0


load_btn = Button(text='Load file', command=Loadfile)
text_check = Checkbutton(text='Text Part', variable=text, onvalue=1, offvalue=0)
img_check = Checkbutton(text='Image Part', variable=img, onvalue=1, offvalue=0)
go_btn = Button(text='Go!', command=main)
filename.grid(row=0, column=0)
load_btn.grid(row=0, column=1)
text_check.grid(row=1, column=1)
img_check.grid(row=2, column=1)
go_btn.grid(row=3, column=3)
t.mainloop()
