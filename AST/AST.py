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
t.title('AST Parser')
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
    """
    Function that creates a log file
    :param status: What Happened
    :param name: Book Name
    :param code: book AST or ASE code
    :param kwargs: link
    :return: ads the event into a log file
    """
    link = kwargs.get('link', None)
    with open('ast.csv', 'a', encoding='utf8') as logs:
        log = csv.writer(logs)
        if link != '':
            log.writerow((status, code, name))
        else:
            log.writerow((status, code, name, link))
    logs.close()


# Gets images and PDF
def get_images(code: str, name1: str):
    name = translit_name(name1)
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}').mkdir(parents=True, exist_ok=True)
    x = 0
    front_cover = f'https://cdn.ast.ru/v2/{code}/COVER/cover1__w600.jpg'
    back_cover = f'https://cdn.ast.ru/v2/{code}/COVER/cover4__w600.jpg'
    pdf = f'https://cdn.eksmo.ru/v2/{code}/PDF/{code}.pdf'
    try:
        urlb.urlretrieve(front_cover, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}/{name}{x}.jpg')
        x += 1
    except urlb1.error.HTTPError:
        log_write("No Front Cover For You :'(", name1[:len(name1) - 1], code)
    try:
        urlb.urlretrieve(back_cover, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}/{name}{x}.jpg')
        x += 1
    except urlb1.error.HTTPError:
        log_write("No Back Cover For You :'(", name1[:len(name1)-1], code)
    try:
        urlb.urlretrieve(pdf, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}/{name}{x}.pdf')
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
    with open("ast_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size'], data['weight'], data['annotation']))


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
        title = soup.select('h1.book-detail__title')[0].text.strip()
    except IndexError:
        log_write('ERROR 404 In Text Parse', name[:len(name)-1], code, link=link)
        return
    page_num1 = soup.find('div', class_='cover-info__text').get_text()
    page_num1 = page_num1.replace(' ', '')
    page_num1 = page_num1.replace('\t', '')
    page_num1 = page_num1.replace('\n', '')
    a = page_num1.find('Вес: ') + 5
    b = page_num1.find(' кг')

    c = page_num1.find('Страниц: ') + 9
    d = page_num1.find('|Размер')

    e = page_num1.find('Размер: ') + 9
    page_num = page_num1[c:d]
    weight = page_num1[a:b]
    isbn = soup.find('div', class_='wrap__col--sm-3').find('div', class_='cover-info__text').get_text()
    isbn = isbn.replace(' ', '/t')
    isbn = isbn.replace('/t', '')
    isbn = isbn.replace('/n', '')
    isbn = isbn[10:27]
    size = page_num1[e:]
    description = ''
    try:
        description = soup.find('div', class_='drop-list__content-body').find('div', class_='text').get_text()
        description = description.replace('\n', '')
        description = description.replace('\t ', '\t')
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
            link = f'https://ast.ru/book/{translit_name(name)}-{code[len(code) - 6:]}/'
            print(f'{link} {y}')
            y += 1
            get_head(get_html(link), name, code, link)
            get_images(code, name)
    elif get_button_info() == 'text':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            link = f'https://ast.ru/book/{translit_name(name)}-{code[len(code) - 6:]}/'
            print(f'{link} {y}')
            get_head(get_html(link), name, code, link)
    elif get_button_info() == 'img':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            print(y)
            get_images(code, name)


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
