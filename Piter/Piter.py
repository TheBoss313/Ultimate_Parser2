from basic_parser_funcs import *
import csv
from time import time

eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
       'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


# Gets images
def get_image(html, name):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find("div", class_="photo").find("img").get("src")
    maged_urls = [title]
    test = soup.find('div', class_='product-links').find_all("a")
    for i in test:
        brewed_url = i.get('href')
        if "iblock" in brewed_url:
            magnified_url = url_magnify_iblock(brewed_url)
            maged_urls.append(magnified_url)
        else:
            maged_urls.append(brewed_url)
    get_images(maged_urls, 'Piter', name, 0, '')
    print(f"FINISHED DOWNLOADING {name}")


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


def piter(filename, text_image):
    print("Starting Piter Download")
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
            # link = 'https://azbooka.ru/books/' + names[j]
            # get_head(get_html(link, name), name, link)
            # get_image(get_html(link, name), name)
    elif text_image == 'text':
        for j in range(len(names)):
            name = translit_name2(names[j], eng)
            # link = 'https://azbooka.ru/books/' + names[j]
            # get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            name = translit_name2(names[j], eng)
            print(name)
            if name.startswith("https:\\"):
                link = name
            else:
                link = 'https://www.piter.com/product_by_id/' + name
            print(link)
            get_image(get_html(link, name), name)
