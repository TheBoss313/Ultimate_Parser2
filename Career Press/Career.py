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
t.title('Careera Press Parser')
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


# Gets images and PDF
def get_images(html, name):
    soup = BeautifulSoup(html, 'lxml')
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/career/{name}').mkdir(parents=True, exist_ok=True)
    x = 0
    try:
        front_cover = soup.find('div', class_='span6 center').find('a', class_='gallery').get('href')
        front_cover = front_cover.replace(u'\ufeff', '')
    except AttributeError:
        log_write("No Front Cover For You :'(", name[:len(name)])
    else:
        urlb.urlretrieve(front_cover,
                         f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/career/{name}/{name}{x}.jpg')

    try:
        pdf = soup.find('div', class_='span8 center').find('a').get('href')
        pdf = str(pdf).replace(u'\ufeff', '')
    except AttributeError:
        try:
            inside = soup.find('div', class_='span-two-thirds').find_all('img')
        except AttributeError:
            log_write('NO INSIDES FOR YOU', name)
        else:
            insides = []
            for i in inside:
                insides.append(i.get('src'))
            for i in insides:
                urlb.urlretrieve(i, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/career/{name}/{name}{x}.jpg')
                x += 1
    else:
        urlb.urlretrieve(pdf, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/career/{name}/{name}{x}.pdf')


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
        title = soup.find('div', class_='span10').find('h1', class_='title').get_text()
    except AttributeError:
        log_write(f'ERROR 404 In Text Parse', name[:len(name)], link=link)
        return
    info_mass = soup.find('div', class_='span10').get_text()
    isbn_n = info_mass.find('ISBN: ')
    isbn = info_mass[isbn_n + 6:isbn_n + 24]
    page_num_n = info_mass.find('Cтраниц: ')
    x = page_num_n + 10
    while True:
        page_num = info_mass[page_num_n + 9:x]
        if page_num.isdigit():
            x += 1
        else:
            x -= 1
            break
    page_num = info_mass[page_num_n + 9:x]
    size_n = info_mass.find('Размеры: ')
    size = info_mass[size_n + 9:size_n + 20]
    if size.endswith(' '):
        size = size[:len(size) - 1]
    description = ''
    try:
        description = soup.find('div', class_='span-two-thirds').get_text()
    except AttributeError:
        log_write('No description for you I guess...', name, link=link)
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size}
    else:
        pass
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size, 'annotation': description}
    csv_read(data)
    log_write('Text Parsed', name[:len(name)])


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
        names.append(i)
    # Checks what is needed
    if get_button_info() == 'textimg':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = f'https://careerpress.ru/book/{name}/'
            link = link.replace(u'\ufeff', '')
            print(f'{link} {y}')
            y += 1
            get_head(get_html(link), name, link)
            get_images(get_html(link), name)
    elif get_button_info() == 'text':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = f'https://careerpress.ru/book/{name}/'
            link = link.replace(u'\ufeff', '')
            print(f'{link} {y}')
            y += 1
            get_head(get_html(link), name, link)
    elif get_button_info() == 'img':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = f'https://careerpress.ru/book/{name}/'
            print(y)
            y += 1
            get_images(link, name)
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
