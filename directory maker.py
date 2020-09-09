from pathlib import Path

rus_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
eng_l = 'abcdefghijklmnopqrstuvwxyz'
eng = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
       'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']
with open('file1.txt', 'r', encoding='utf8') as file:
    lost = file.readlines()
file.close()


# Translits name for link
def translit(name: str):
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
    if end_name.startswith('-'):
        end_name = end_name[1:]
    return end_name


print(*lost)
a = input('CONTINUE?')
for i in range(len(lost)):
    '''i = i.split('.', 1)
    try:
        i = i[1]
    except IndexError:
        i = i[0]'''
    # Excel Equivalent:
    # =IF(IF(IFERROR(FIND(".",RC[-9],1),0)>0,RIGHT(RC[-9],LEN(RC[-9])-(IFERROR(FIND(".",RC[-9],1),0))))=FALSE,RC[-9],IF(IFERROR(FIND(".",RC[-9],1),0)>0,RIGHT(RC[-9],LEN(RC[-9])-(IFERROR(FIND(".",RC[-9],1),0)))))
    # i = translit(i)
    Path(f'C:/Users/Vlad/Desktop/Machaon Downloaded 2020-08-11/{i}').mkdir(parents=True, exist_ok=True)
