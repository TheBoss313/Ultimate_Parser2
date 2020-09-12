import urllib.request as urlb
import csv
from basic_parser_funcs import *
from text_cleanup import *
from bs4 import BeautifulSoup

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


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
def get_all_rech(html, name):
    soup = BeautifulSoup(html, 'lxml')
    a = soup.findAll('table')[1].findAll('tr')
    insides = []
    title = ''
    pages = 0
    size = ''
    cover = ''
    isbn = ''
    description = ''
    for tr in range(len(a)):
        b = a[tr].findAll('td')
        for td in range(len(b)):
            if tr == 0 and td == 0:
                for d in b[td].find_all('a', href=True):
                    insides.append(d['href'])
            elif tr == 0 and td == 1:
                for d in b[td].find_all('h1'):
                    title = d.text.strip()
                e = b[td].find('div', class_='left').text.strip()
                e = e.replace('  ', '').replace('\t', '')
                ee = e.split('\n')
                for eee in ee:
                    if 'Объем: ' in eee:
                        pages = (eee[eee.find('Объем: ') + len('Объем: '):])
                    elif 'Формат: ' in eee:
                        size = (eee[eee.find('Формат: ') + len('Формат: '):])
                    elif 'Тип переплета: ' in eee:
                        cover = (eee[eee.find('Тип переплета: ') + len('Тип переплета: '):])
                    elif 'ISBN: ' in eee:
                        isbn = (eee[eee.find('ISBN: ') + len('ISBN: '):])
                    else:
                        pass
            elif tr == 1 and td == 0:
                for d in b[td].find_all('img'):
                    insides.append(d.get('src'))
            elif tr == 1 and td == 1:
                description = b[td].text.strip()
                description = empty_lines(description)
    data = {'title': title, 'pages': pages, 'cover': cover, 'size': size, 'isbn': isbn, 'desc': description}
    for i in range(len(insides)):
        Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/rech/{name}').mkdir(parents=True, exist_ok=True)
        urlb.urlretrieve(f'http://www.rech-deti.ru/{insides[i]}', f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser'
                                                                  f'/images/rech/{name}/{i}.jpg')


def main(filename, text_image):
    links = []
    names = []
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        sub_tot = i.split(',', 1)
        links.append(sub_tot[0])
        names.append(sub_tot[1])
    for j in range(len(names)):
        link = links[j]
        name = names[j]
        get_all_rech(get_html(link, name), name)
