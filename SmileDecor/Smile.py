from basic_parser_funcs import *
from text_cleanup import *
import csv
publisher_name = 'Smile_Decor'
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
    cover = ['https://smile-decor.ru'+i.get('href') for i in soup.find('div', class_='slides').find_all('a', class_='fancy')]
    get_images(cover, publisher_name, name, 0)


# Writes the info into CSV file
def csv_read(data):
    with open(r"csvs\smile_decor_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['mass'], data['desc']))
    file.close()


# Gets the info from soup
def get_head(html, name, link):
    soup = BeautifulSoup(html, 'lxml')
    name2 = soup.find('div', class_='dotdot').text
    p_tag1 = soup.find('div', class_='detail_text').text
    mass = empty_lines(soup.find('table', class_='nbg').find_all('tr')[1].find('td', class_='char_value').text)
    data = {'name': name2, 'mass': mass, 'desc': p_tag1}
    csv_read(data)
    log_file('Text Parsed', name[:len(name)], link=link)


def smile(filename, text_image):
    names = []
    urls = []
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        urls.append(i.split(',', 1)[0])
        names.append(i.split(',', 1)[1])
    # Checks what is needed
    if text_image == 'textimg':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = urls[j]
            get_head(get_html(link, name), name, link)
            get_image(get_html(link, name), name)
    elif text_image == 'text':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = urls[j]
            get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = urls[j]
            get_image(get_html(link, name), name)