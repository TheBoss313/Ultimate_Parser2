# info: class_ = 'more-book-info'
#       get all spans
# Description: class_ = 'book-description'
#       get p
# Cover: div class_ = 'book-cover'
#       get 'href'

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as ms
import urllib.request as urlb
import urllib as urlb1
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import csv

t = Tk()
t.title('Kompas Gid Parser')
t.resizable(False, False)
filename_name = ''
filename = Label(t, text='NO FILE SELECTED')
y = 1
names = []
errors = []
text = IntVar()
img = IntVar()
rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
       'f', 'kh', 'ts', 'ch', 'sh', 'sh', '', 'y', '', 'e', 'yu', 'ya']


def log_write(status, name, **kwargs):
    link = kwargs.get('link', None)
    with open('career.csv', 'a', encoding='utf8') as logs:
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
    end_name = end_name.replace('--', '-')
    return end_name


# Loads file
def loadFile():
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
    with open("career_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        try:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size'], data['annotation']))
        except KeyError:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size']))
    file.close()


# Gets the HTML from URL
def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    log_write('Html Loading Successful', url)
    return r.text


# Gets the info from soup
def get_head(html, name, link):
    soup = BeautifulSoup(html, 'lxml')
    title = ''
    try:
        title = soup.find('div', class_='book-title').get('h1')
    except AttributeError:
        log_write(f'ERROR 404 In Text Parse', name[:len(name)], link=link)
        return
    info_mass1 = soup.find('div', class_='row').find_all('div', class_='more-book-info')
    info_mass = []
    for i in info_mass1:
        a = i.find_all('span')
        for j in a:
            info_mass.append(j.get_text())
    print(info_mass[2], info_mass[3], info_mass[4])
    isbn = info_mass[2]
    page_num = info_mass[3]
    mass = info_mass[4]
    '''x = page_num.find('Кол-во страниц: ')+1
    while True:
        page_num = info_mass[x:x]
        if page_num.isdigit():
            x += 1
        else:
            x -= 1
            break
    description = ''
    try:
        description = soup.find('div', class_='span-two-thirds').get_text()
    except AttributeError:
        log_write('No description for you I guess...', name, link=link)
        data = {'title': title, 'pagen': page_num, 'mass':mass, 'ISBN': isbn}
    else:
        pass
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'mass':mass, 'annotation': description}
    csv_read(data)
    log_write('Text Parsed', name[:len(name)])'''


def main():
    global y
    # Gets info from file
    with open(filename_name, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        names.append(i)
    # Checks what is needed
    for i in names:
        name1 = translit_name(i)
        link = f'https://www.kompasgid.ru/ru/knigi/{name1}'
        get_head(get_html(link), name1, link)


'''load_btn = Button(text='Load file', command=loadFile)
text_check = Checkbutton(text='Text Part', variable=text, onvalue=1, offvalue=0)
img_check = Checkbutton(text='Image Part', variable=img, onvalue=1, offvalue=0)
go_btn = Button(text='Go!', command=main)
filename.grid(row=0, column=0)
load_btn.grid(row=0, column=1)
text_check.grid(row=1, column=1)
img_check.grid(row=2, column=1)
go_btn.grid(row=3, column=3)'''
get_head(get_html('https://www.kompasgid.ru/ru/knigi/ya-hotel-ubit-nebo-avtobiografiya-kabachka'), 'Name1',
         'https://www.kompasgid.ru/ru/knigi/ya-hotel-ubit-nebo-avtobiografiya-kabachka')
# t.mainloop()
