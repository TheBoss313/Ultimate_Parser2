import urllib.request as urlb
import urllib as urlb1
import csv
from basic_parser_funcs import *

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


# Gets images and PDF
def get_images(code: str, name1: str):
    name = translit_name(name1)
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}').mkdir(parents=True, exist_ok=True)
    x = 0
    front_cover = f'https://cdn.ast.ru/v2/{code}/COVER/cover1__w600.jpg'
    back_cover = f'https://cdn.ast.ru/v2/{code}/COVER/cover4__w600.jpg'
    pdf = f'https://cdn.eksmo.ru/v2/{code}/PDF/{code}.pdf'
    print(front_cover)
    try:
        urlb.urlretrieve(front_cover, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}/{name}{x}.jpg')
        x += 1
    except urlb1.error.HTTPError:
        log_file("No Front Cover For You :'(", name1[:len(name1) - 1])
    try:
        urlb.urlretrieve(back_cover, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}/{name}{x}.jpg')
        x += 1
    except urlb1.error.HTTPError:
        log_file("No Back Cover For You :'(", name1[:len(name1)-1])
    try:
        urlb.urlretrieve(pdf, f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/ast/{name}/{name}{x}.pdf')
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
    with open(r"csvs\ast_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        try:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size'], data['weight'], data['annotation']))
        except KeyError:
                writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size'], data['annotation']))


# Gets the info from soup
def get_head(html, name, link):
    soup = BeautifulSoup(html, 'lxml')
    title = ''
    try:
        title = soup.select('h1.book-detail__title')[0].text.strip()
    except IndexError:
        log_file('ERROR 404 In Text Parse', name[:len(name)-1], link=link)
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
        log_file('No description for you I guess...', name, link=link)
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size}
    else:
        data = {'title': title, 'pagen': page_num, 'ISBN': isbn, 'size': size, 'annotation': description}
    csv_read(data)
    log_file('Text Parsed', name[:len(name)-1])


def ast(filename, text_image):
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    codes = []
    names = []
    for i in lines:
        sub_tot = i.split(',', 1)
        codes.append(sub_tot[0])
        names.append(sub_tot[1])
    # Checks what is needed
    if text_image == 'textimg':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            link = f'https://ast.ru/book/{translit_name(name)}-{code[len(code) - 6:]}/'
            get_head(get_html(link, name), name, link)
            get_images(code, name)
    elif text_image == 'text':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            link = f'https://ast.ru/book/{translit_name(name)}-{code[len(code) - 6:]}/'
            get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            code = codes[j]
            name = names[j]
            get_images(code, name)
