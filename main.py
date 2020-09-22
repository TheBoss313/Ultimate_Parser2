from basic_parser_funcs import *
from ROSMAN.ROSMEN import rosman
from AST.AST import ast
from EKSMO.EKSMO import eksmo
from Career.Career import career
from Rech.Rech import rech
from Nigma.Nigma import nigma
from MIF.Mif import mif

# Important Variables
filename = ''
done = ['ROSMAN', 'AST', 'EKSMO', 'Career Press', 'Rech', 'Nigma', 'Mif']
format_descriptions = {'ROSMAN': 'Format:\n',
                       'AST': 'Format:\n{AST/ASE code},{Book Name}',
                       'EKSMO': 'Format:\n{AST/ASE code},{Book Name}',
                       'Career Press': 'Format:\nBook Names',
                       'Rech': 'Format:\n{url},{Book Name}',
                       'Nigma': 'Format:\n{url},{Book Name}',
                       'Mif': 'Format\n{name}',
                       'No Publisher\nChosen': ''
                       }


# Returns textimg text img depending on checked CheckButtons
def get_button_info():
    global text, img
    strong = ''
    if text.get() == 1:
        strong = strong + 'text'
    if img.get() == 1:
        strong = strong + 'img'
    if strong == '':
        ms.showerror('NO OPTION SELECTED', 'PLEASE SELECT TEXT, IMAGES OR BOTH!')
        return 'ERROR'
    return strong


def ultra_main():
    text_image = get_button_info()
    publisher_use = publisher.get()
    if publisher_use == 'ROSMAN':
        rosman(filename, text_image)
    elif publisher_use == 'AST':
        ast(filename, text_image)
    elif publisher_use == 'EKSMO':
        eksmo(filename, text_image)
    elif publisher_use == 'Career Press':
        career(filename, text_image)
    elif publisher_use == 'Rech':
        rech(filename, text_image)
    elif publisher_use == 'Nigma':
        nigma(filename, text_image)
    elif publisher_use == 'Mif':
        mif(filename, text_image)


def load():
    global filename
    filename = Loadfile()
    loaded = Path(filename).name
    filename1.config(text=loaded)


def format_disp():
    tk = Tk()
    l1 = Label(tk, text=format_descriptions[publisher.get()])
    l1.pack()


# Tkinter GUI Part
t = Tk()
t.title('Ultimate Parser')
t.resizable(False, False)
publisher = StringVar(t)
publisher.set("No Publisher\nChosen")  # default value
text = IntVar()
img = IntVar()
w = OptionMenu(t, publisher, *done)
filename1 = Label(t, text='NO FILE SELECTED')
load_btn = Button(t, text='Load file', command=load)
text_check = Checkbutton(t, text='Text Part', variable=text, onvalue=1, offvalue=0)
img_check = Checkbutton(t, text='Image Part', variable=img, onvalue=1, offvalue=0)
go_btn = Button(t, text='Go!', command=ultra_main)
format_b = Button(t, text='File Input\nFormat', command=format_disp)
filename1.grid(row=0, column=0)
load_btn.grid(row=0, column=1)
w.grid(row=1, column=0)
text_check.grid(row=1, column=1)
img_check.grid(row=2, column=1)
format_b.grid(row=2, column=0)
go_btn.grid(row=3, column=3)
t.mainloop()
