import urllib.request as urlb
import urllib.error as urlbr
from pathlib import Path

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']


def parse(num_first: int, name, num: int = 4):
    Path(f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/r_ftp/{translit_name(name)}') \
        .mkdir(parents=True, exist_ok=True)

    for i in range(num):
        try:
            urlb.urlretrieve(f'ftp://rosmanpictures@ftp.rosman.ru/{num_first + i}.jpg',
                             f'C:/Users/Vlad/PycharmProjects/Ultimate_Parser/images/r_ftp/'
                             f'{translit_name(name)}/{num_first + i}.jpg')
        except urlbr.URLError:
            pass


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


def main_ftp(lines):
    for line in lines:
        code = line.split(',', 1)[0].lower().replace('.jpg', '').replace('ftp://rosmanpictures@ftp.rosman.ru/', '')
        name = line.split(',', 1)[1]
        parse(int(code), name, 4)
