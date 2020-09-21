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
    cover = soup.find('div', class_='img-wrapper').find('img').get('src')
    cover = ('https://www.mann-ivanov-ferber.ru'+cover).replace('1.00x', '2.00x')
    get_images([cover], 'Mif', name, 0)
    pdf = soup.find('div', class_='img-wrap').find('a').get('modal-params')
    pdf = pdf[pdf.find('https:'):pdf.find('.pdf')+4].replace('_stamped', '')
    get_pdf(pdf, 'Mif', name, 1)
    pdf2 = soup.find('div', class_='nkk-file-download').find('a').get('href').replace('_stamped', '')
    get_pdf(pdf2, 'Mif', name, 2)


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
    p_tag1 = soup.find('div', class_="content")
    ISBN = ''
    pages = ''
    size = ''
    cover = ''
    print(p_tag1)


def mif(filename, text_image):
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
