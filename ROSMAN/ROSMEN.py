import csv
from basic_parser_funcs import *

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
    with open(r"csvs\rosman_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['annotation']))


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


def get_image(html, name, tk):
    name1 = translit_name(name)
    soup = BeautifulSoup(html, 'lxml')
    try:
        imgs1 = soup.find('div', class_='item-pic-pre').find_all('div')
    except AttributeError:
        url = ask_for_manual_url(name, tk)
        html = get_html(url, name1)
        soup = BeautifulSoup(html, 'lxml')
    imgs = soup.find('div', class_='item-pic-pre')
    links = ['https://rosman.ru'+i.get('id') for i in imgs.find_all('div', 'item-pic-pre-one')]
    links = [i.replace('resize_cache/', '').replace('700_700_1/', '') for i in links]
    get_images(links, 'Rosman', 'name', 0)
    log_file('Images Parsed', name1)


def rosman(filename, button_info, tk):
    names = []
    links = []
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for line in lines:
        names.append(line)
    # Checks what is needed
    if button_info == 'textimg':
        for j in range(len(names)):
            name = names[j]
            link = f'https://rosman.ru/catalog/item/{translit_name(name)}/'
            hatmail = get_html(link, name)
            get_image(hatmail, translit_name(name), tk)
            get_head(hatmail, name)
    elif button_info == 'text':
        for j in range(len(names)):
            name = names[j]
            link = f'https://rosman.ru/catalog/item/{translit_name(name)}/'
            hatmail = get_html(link, name)
            get_head(hatmail, name)
    elif button_info == 'img':
        for j in range(len(names)):
            name = names[j].replace('\n', '')
            link = f'https://rosman.ru/catalog/item/{translit_name(name)}/'
            hatmail = get_html(link, translit_name(name))
            get_image(hatmail, name, tk)
