from tkinter import *

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_AST = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
           'f', 'kh', 'ts', 'ch', 'sh', 'w', '', 'y', '', 'e', 'yu', 'ya']
eng_ROSMAN = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
              'f', 'kh', 'ts', 'ch', 'sh', 'w', '', 'y', '', 'e', 'yu', 'ya']
eng_CAREER = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
              'f', 'kh', 'ts', 'ch', 'sh', 'w', '', 'y', '', 'e', 'yu', 'ya']
eng_l = 'abcdefghijklmnopqrstuvwxyz'


def translit_name1():
    name = input('NAME(RU): ')
    test = input('LINK(TEN): ')
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
            end_name = end_name + eng_CAREER[a]
        elif name[i].isdigit():
            end_name = end_name + name[i]
    end_name = end_name.replace('--', '-')
    end_name = end_name.replace('--', '-')
    if test == end_name:
        print('SAME')
    else:
        print(f'{test}, {end_name}')


while True:
    translit_name1()
