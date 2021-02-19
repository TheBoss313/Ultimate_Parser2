from basic_parser_funcs import *
from text_cleanup import *
import csv

eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
       'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


# Gets images
def get_image(html, name):
    soup = BeautifulSoup(html, 'lxml')
    maged_urls = []
    for i in soup.find_all('div', class_='_9XL-sKqTDl'):
        brewed_url = i.find('img').get('src')
        magnified_url = url_magnify_iblock(brewed_url)
        maged_urls.append(magnified_url)
    get_images(maged_urls, 'Machaon', name, 0, '')


# Writes the info into CSV file
def csv_read(data):
    with open(r"csvs\machaon_parsed.csv", 'a', encoding="utf-8")as file:
        writer = csv.writer(file)
        try:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size'], data['annotation']))
        except KeyError:
            writer.writerow((data['title'], data['ISBN'], data['pagen'], data['size']))
    file.close()


# Gets the info from soup
def get_head(html, name, link):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', class_='VKrmQXOtBg')
    print(soup.find('div', class_='_19tSXSSOSx'))
    print(soup.select_one('._1YUztduJR8'))
    '''
    tag = soup.find('div', class_='_19tSXSSOSx').find_all('div', class_='_1YUztduJR8')
    ISBN = tag[4]
    pages = tag[2]
    size = tag[3]
    cover = tag[1]
    try:
        p_tag4 = soup.find('div', class_='wth2ozwagb')
        description = str(p_tag4.find('p')).replace('<br/>', '\n').replace('<span>', '').replace('</span>', '')
    except AttributeError:
        log_file('No description for you I guess...', name, link=link)
        data = {'title': title, 'pagen': pages, 'ISBN': ISBN, 'size': size, 'cover': cover}
    else:
        pass
        data = {'title': name, 'pagen': pages, 'ISBN': ISBN, 'size': size, 'annotation': description, 'cover': cover}
    print(data)
    # csv_read(data)
    # log_file('Text Parsed', name[:len(name)])'''


def machaon(filename, text_image):
    print("Starting Machaon Download")
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
            name = translit_name2(names[j], eng)
            #link = 'https://azbooka.ru/books/' + names[j]
            #get_head(get_html(link, name), name, link)
            #get_image(get_html(link, name), name)
    elif text_image == 'text':
        for j in range(len(names)):
            name = translit_name2(names[j], eng)
            #link = 'https://azbooka.ru/books/' + names[j]
            #get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            name = translit_name2(names[j], eng)
            print(name)
            link = 'https://azbooka.ru/books/' + name
            print(link)
            get_image(get_html(link, name), name)
