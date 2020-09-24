from basic_parser_funcs import *
import csv

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
       'f', 'h', 'ts', 'ch', 'sh', 'shh', '', 'y', '', 'e', 'yu', 'ya']


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
    cover = ('https://www.mann-ivanov-ferber.ru' + cover).replace('1.00x', '2.00x')
    get_images([cover], 'Mif', name, 0)
    try:
        insides = ['https://www.mann-ivanov-ferber.ru/' + i.find('img').get('hires-src') for i in soup.find('section',
                                id='imageslist').find('div', class_='slider-pane').find_all('div', class_='slider-item')]
        get_images(insides, 'Mif', name, 1)
    except AttributeError:
        pdf = soup.find('div', class_='img-wrap').find('a').get('modal-params')
        pdf = pdf[pdf.find('https:'):pdf.find('.pdf')+4].replace('_stamped', '')
        get_pdf(pdf, 'Mif', name, 1)


# Writes the info into CSV file
def csv_read(data):
    with open(r"csvs\mif_parsed.csv", 'a', encoding="utf-8")as file:
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
    # Gets info from file
    with open(filename, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()
    for i in lines:
        names.append(translit_name(i))
    # Checks what is needed
    if text_image == 'textimg':
        ms.showerror('Development', 'Info parser is still under development.\nOnly images available.')
        return
        for j in range(len(names)):
            name = translit_name(names[j])
            link = urls[j]
            get_head(get_html(link, name), name, link)
            get_image(get_html(link, name), name)
    elif text_image == 'text':
        ms.showerror('Development', 'Info parser is still under development.\nOnly images available.')
        return
        for j in range(len(names)):
            name = translit_name(names[j])
            link = urls[j]
            link = link.replace(u'\ufeff', '')
            get_head(get_html(link, name), name, link)
    elif text_image == 'img':
        for j in range(len(names)):
            name = names[j]
            link = f'https://www.mann-ivanov-ferber.ru/books/{name}/'
            get_image(get_html(link, name), name)
