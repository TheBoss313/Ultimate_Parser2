import pyautogui as pag


def ctrl_c():
    pag.keyDown('ctrl')
    pag.press('c')
    pag.keyUp('ctrl')


def ctrl_l():
    pag.keyDown('ctrl')
    pag.press('l')
    pag.keyUp('ctrl')


def ctrl_a():
    pag.keyDown('ctrl')
    pag.press('a')
    pag.keyUp('ctrl')


def ctrl_v():
    pag.keyDown('ctrl')
    pag.press('v')
    pag.keyUp('ctrl')


def ctrl_t():
    pag.keyDown('ctrl')
    pag.press('t')
    pag.keyUp('ctrl')


def ctrl_tab():
    pag.keyDown('ctrl')
    pag.press('tab')
    pag.keyUp('ctrl')


def close_tab():
    pag.keyDown('ctrl')
    pag.press('w')
    pag.keyUp('ctrl')


def alt_tab():
    pag.keyDown('alt')
    pag.press('tab')
    pag.keyUp('alt')


def ctrl_ctv():
    ctrl_c()
    ctrl_t()
    ctrl_v()
    pag.press('enter')
    ctrl_tab()


def save_img():
    pag.leftClick(956, 522)
    pag.rightClick(956, 522)
    pag.leftClick(1089, 582)
    pag.sleep(3)
    pag.press('enter')


def save_pdf():
    pag.moveTo(1750, 200)
    pag.sleep(1)
    pag.click()
    pag.sleep(10)
    pag.press('enter')


def open1(event):
    alt_tab()
    ctrl_ctv()


def save_img_f(event):
    alt_tab()
    save_img()
    close_tab()
    alt_tab()


def save_pdf_f(event):
    alt_tab()
    save_pdf()
    close_tab()
    alt_tab()
