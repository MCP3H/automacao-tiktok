import webbrowser
import pyautogui as pyg
import pyperclip


def abrirTiktokTag(param):
    param = param.replace(" ", "")
    webbrowser.open("https://www.tiktok.com/tag/" + param)


def abrirLocalhost():
    webbrowser.open("http://127.0.0.1:5000/")


def abrirMidia():
    pyg.click(x=450, y=560, duration=0.5)


def fecharMidia():
    pyg.click(x=50, y=135, duration=0.5)


def curtirVideo():
    pyg.doubleClick(x=620, y=550, duration=0.5)


def passarVideo():
    pyg.click(x=1190, y=570, duration=0.5)


def copiarLinkVideo():
    pyg.click(x=1190, y=65)
    pyg.hotkey("ctrl", "c")
    link = pyperclip.paste()
    return link


def fecharTiktok():
    pyg.click(x=1890, y=20, duration=0.5)
