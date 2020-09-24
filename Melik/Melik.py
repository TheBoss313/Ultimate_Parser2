from basic_parser_funcs import *
from text_cleanup import *
import csv

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
       'f', 'kh', 'ts', 'ch', 'sh', 'sh', '', 'y', '', 'e', 'yu', 'ya']


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


# Gets images
def get_image(html, name):
    soup = BeautifulSoup(html, 'lxml')
    cover = soup.find('img', class_='book-border').get('src')
    cover = cover[:cover.rfind('?')]
    insides = soup.find('div', class_='cycle-slideshow').find_all('a')
    insides = [i.get('href')[:i.get('href').rfind('?')] for i in insides]
    get_images([cover]+insides, 'Melik', name, 0)


# Writes the info into CSV file
def csv_read(data):
    with open(r"csvs\melik_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['size'], data['pages'], data['cover'], data['desc']))
    file.close()


# Gets the info from soup
def get_head(html, name, link):
    soup = BeautifulSoup(html, 'lxml')
    p_tag1 = soup.find('div', id='main-col').find('div', class_='row').find_all('div', class_='row')
    name2 = p_tag1[0].find('h4').text
    info = p_tag1[0].find_all('div', class_='grey')
    info = [i.text for i in info]
    cover = info[0]
    pages = info[1]
    size = info[2]
    desc = str(p_tag1[2].find('div', "readmore-book-description")).replace('</p>', '\n')
    desc = desc.replace('<div class="readmore-book-description">', '').replace('<p>', '').replace('</div>', '')
    desc = empty_lines(desc)
    data = {'name': name2, 'size': size, 'pages': pages, 'cover': cover, 'desc': desc}
    csv_read(data)
    log_file('Text Parsed', name[:len(name)], link=link)


def melik(filename, text_image):
    names = []
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        names.append(i)
    # Checks what is needed
    if text_image == 'textimg':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = f'http://www.melik-pashaev.ru/books/{name}'
            get_head(get_html(link, name), name, link)
            get_image(get_html(link, name), name)
    elif text_image == 'text':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = f'http://www.melik-pashaev.ru/books/{name}'
            get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = f'http://www.melik-pashaev.ru/books/{name}'
            get_image(get_html(link, name), name)
