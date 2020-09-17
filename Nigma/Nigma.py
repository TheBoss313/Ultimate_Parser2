from basic_parser_funcs import *
from text_cleanup import *
import csv

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
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
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/Nigma/{name}').mkdir(parents=True, exist_ok=True)
    p_tag3 = soup.find('div', class_='wrap-img-book').find('img').get('src')
    p_tag2 = soup.find('section', class_='grid-wrap')
    p_tag2s = p_tag2.findAll('li')
    p_tag2s2 = [i.find('img').get('src') for i in p_tag2s[1:]]
    get_images([p_tag3]+p_tag2s2, 'Nigma', name, 0)


# Writes the info into CSV file
def csv_read(data):
    with open("nigma_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        try:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size'], data['annotation']))
        except KeyError:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size']))
    file.close()


# Gets the info from soup
def get_head(html, name, link):
    soup = BeautifulSoup(html, 'lxml')
    p_tag1 = soup.find('ul', class_='descs-book')
    ISBN = ''
    pages = ''
    size = ''
    cover = ''
    for i in p_tag1.findAll('li'):
        try:
            i.find('span').text
        except AttributeError:
            log_file('Critical', 'Nigma Empty Span')
        else:
            if i.find('span').text in ['Артикул', 'Издатель', 'Авторы', 'Иллюстраторы', 'Год', 'Формат']:
                pass
            else:
                if not i.find('div'):
                    spans = i.findAll('span')
                    string = spans[1].text.strip()
                    string = string.replace(' ', '')
                    string = empty_lines(string).replace('/n', '')
                    if spans[0] == '':
                        pass
                    elif spans[0].text == 'ISBN':
                        ISBN = string
                    elif spans[0].text == 'К-во страниц':
                        pages = string
                    elif spans[0].text == 'Переплет':
                        cover = string
                else:
                    if 'Размер (мм)' in i.text:
                        size = i.text[i.text.find('Размер (мм)') + len('Размер (мм)'):]
        description = ''
        try:
            p_tag4 = soup.find('div', class_='wrap-annotation-book')
            description = str(p_tag4.find('span')).replace('<br/>', '\n').replace('<span>', '').replace('</span>', '')
        except AttributeError:
            log_file('No description for you I guess...', name, link=link)
            data = {'title': name, 'pagen': pages, 'ISBN': ISBN, 'size': size}
        else:
            pass
            data = {'title': name, 'pagen': pages, 'ISBN': ISBN, 'size': size, 'annotation': description}
        csv_read(data)
        log_file('Text Parsed', name[:len(name)])


def nigma(filename, text_image):
    names = []
    urls = []
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        urls.append(i.split(',')[0])
        names.append(i.split(',')[1])
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
            link = link.replace(u'\ufeff', '')
            get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            name = translit_name(names[j])
            link = urls[j]
            get_image(get_html(link, name), name)
