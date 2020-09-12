import urllib.request as urlb
import urllib as urlb1
import csv
from basic_parser_funcs import *

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


def shorten(code):
    if code[4] != '0':
        return code[:3]+code[4:]
    else:
        return shorten(code[:3]+code[4:])


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
        log_file("No Front Cover For You :'(", name1[:len(name1) - 1])
    try:
        urlb.urlretrieve(back_cover, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/eksmo/{name}/{name}{x}.jpg')
        x += 1
    except urlb1.error.HTTPError:
        log_file("No Back Cover For You :'(", name1[:len(name1)-1])
    try:
        urlb.urlretrieve(pdf, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/eksmo/{name}/{name}{x}.pdf')
    except urlb1.error.HTTPError:
        log_file("No PDF For You :'(", name1[:len(name1)-1])
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


# Writes the info into CSV file
def csv_read(data):
    with open("eksmo_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        try:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size'], data['annotation']))
        except KeyError:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size']))
    file.close()


# Gets the info from soup
def get_head(html, name, link):
    soup = BeautifulSoup(html, 'lxml')
    title = ''
    try:
        title = soup.select('h1.book-card__title')[0].text.strip()
    except IndexError:
        log_file('ERROR 404 In Text Parse', name[:len(name)-1], link=link)
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
        log_file('No description for you I guess...', name, link=link)
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size}
    else:
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size, 'annotation': description}
    csv_read(data)
    log_file('Text Parsed', name[:len(name)-1])


def eksmo(filename, text_image):
    codes = []
    names = []
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        sub_tot = i.split(',', 1)
        codes.append(sub_tot[0])
        names.append(sub_tot[1])
    # Checks what is needed
    if text_image == 'textimg':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            link = f'https://eksmo.ru/book/{translit_name(name)}-{code}/'
            link = link.replace(u'\ufeff', '')
            get_head(get_html(link, name), name, link)
            get_images(code, name)
    elif text_image == 'text':
        for j in range(len(names)):
            code = codes[j]
            code = shorten(code)
            name = names[j]
            link = f'https://eksmo.ru/book/{translit_name(name)}-{code}/'
            link = link.replace(u'\ufeff', '')
            get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            get_images(code, name)
