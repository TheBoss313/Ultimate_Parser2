from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as ms
import urllib.request as urlb
import urllib as urlb1
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import csv
# 103
t = Tk()
t.title('EKSMO Parser')
t.resizable(False, False)
filename_name = ''
filename = Label(t, text='NO FILE SELECTED')
y = 1
codes = []
names = []
errors = []
text = IntVar()
img = IntVar()
rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


def log_write(status, name, code, **kwargs):
    link = kwargs.get('link', None)
    with open('eksmo.csv', 'a', encoding='utf8') as logs:
        log = csv.writer(logs)
        if link != '':
            log.writerow((status, code, name))
        else:
            log.writerow((status, code, name, link))
    logs.close()


# Gets images and PDF
def get_images(code: str, name1: str):
    if code.startswith('430'):
        code1 = code.replace('430', '430000000000')
    else:
        code1 = code.replace('ITD', 'ITD000000000')
    if len(code1) > 18:
        while len(code1) > 18:
            a = code1.find('0')
            code1 = code1[:a] + code1[a+1:]
    name = translit_name(name1)
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/eksmo/{name}').mkdir(parents=True, exist_ok=True)
    x = 0
    front_cover = f'https://cdn.eksmo.ru/v2/{code1}/COVER/cover1__w600.jpg'.replace(u'\ufeff', '')
    back_cover = f'https://cdn.eksmo.ru/v2/{code1}/COVER/cover4__w600.jpg'.replace(u'\ufeff', '')
    pdf = f'https://cdn.eksmo.ru/v2/{code1}/PDF/{code1}.pdf'.replace(u'\ufeff', '')
    try:
        urlb.urlretrieve(front_cover,
                         f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/eksmo/{name}/{name}{x}.jpg')
        x += 1
    except urlb1.error.HTTPError:
        log_write("No Front Cover For You :'(", name1[:len(name1) - 1], code)
    try:
        urlb.urlretrieve(back_cover, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/eksmo/{name}/{name}{x}.jpg')
        x += 1
    except urlb1.error.HTTPError:
        log_write("No Back Cover For You :'(", name1[:len(name1)-1], code)
    try:
        urlb.urlretrieve(pdf, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/eksmo/{name}/{name}{x}.pdf')
    except urlb1.error.HTTPError:
        log_write("No PDF For You :'(", name1[:len(name1)-1], code)
        return


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
    log_write('File Load Successful', filename2.name, '')


# Writes the info into CSV file
def csv_read(data):
    with open("eksmo_parsed.csv", 'a', encoding="utf-8")as file:
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
    log_write('Html Loading Successful', url, '')
    return r.text


# Gets the info from soup
def get_head(html, name, code, link):
    soup = BeautifulSoup(html, 'lxml')
    title = ''
    try:
        title = soup.select('h1.book-card__title')[0].text.strip()
    except IndexError:
        log_write('ERROR 404 In Text Parse', name[:len(name)-1], code, link=link)
        return
    page_num1 = soup.find('div', class_='book-card__params').find_all('div', class_='book-card__params-item')
    page_num = str(page_num1[2])
    a = page_num.rfind(' ')
    d = page_num.find('>') + 1
    page_num = page_num[d:a]
    isbn = soup.find('span', class_='copy__val').get_text()
    size = page_num1[1].get_text()
    b = size.find('(') + 1
    c = size.find(')')
    size = size[b:c]
    description = ''
    try:
        description = soup.find('div', class_='spoiler__text').get_text()
    except AttributeError:
        log_write('No description for you I guess...', name, code, link=link)
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size}
    else:
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size, 'annotation': description}
    csv_read(data)
    log_write('Text Parsed', name[:len(name)-1], code)


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
    global y
    # Gets info from file
    with open(filename_name, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        sub_tot = i.split(',', 1)
        codes.append(sub_tot[0])
        names.append(sub_tot[1])
        print(sub_tot[1])
    # Checks what is needed
    if get_button_info() == 'textimg':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            link = f'https://eksmo.ru/book/{translit_name(name)}-{code}/'
            link = link.replace(u'\ufeff', '')
            print(f'{link} {y}')
            y += 1
            get_head(get_html(link), name, code, link)
            get_images(code, name)
    elif get_button_info() == 'text':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            link = f'https://eksmo.ru/book/{translit_name(name)}-{code}/'
            link = link.replace(u'\ufeff', '')
            print(f'{link} {y}')
            y += 1
            get_head(get_html(link), name, code, link)
    elif get_button_info() == 'img':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            print(y)
            y += 1
            get_images(code, name)
    else:
        pass
    for r in errors:
        for c in r:
            print(c, end=" ")
        print()


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
