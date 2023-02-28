import webbrowser
import pyautogui as pyg
import time
import numpy as np
from PIL import ImageGrab
import pyperclip

_delayFuncao = 1


def abrirTiktok():
    webbrowser.open('https://www.tiktok.com/')
    time.sleep(5)


# def entrarConta():
#     # mouse botão "Entrar"
#     pyg.click(x=1530, y=130)
#     time.sleep(1)
#     # mouse "Usar telefone/e-mail/nome de usuário"
#     pyg.click(x=935, y=435)
#     time.sleep(1)
#     # mouse "Entrar com nome de usuário ou e-mail"
#     pyg.click(x=1070, y=350)
#     time.sleep(1)
#     # inserindo e-mail
#     pyg.click(x=740, y=400)
#     pyg.write('automacaotiktok@gmail.com', interval='0.2')
#     time.sleep(1)
#     # inserindo senha
#     pyg.click(x=740, y=460)
#     pyg.write('automacao10!', interval='0.2')
#     time.sleep(1)
#     # mouse "Entrar"
#     pyg.click(x=960, y=590)


def abrirMidia():
    time.sleep(_delayFuncao)
    pyg.click(x=1055, y=700, duration=0.5)


def fecharMidia():
    time.sleep(_delayFuncao)
    pyg.click(x=50, y=135, duration=0.5)


def curtirVideo():
    time.sleep(_delayFuncao)
    # coracaoLocation = pyg.locateCenterOnScreen('img/coracao.png')
    # if(coracaoLocation != 'None'):
    #     pyg.moveTo(x=coracaoLocation.x, y=coracaoLocation.y, duration=0.5)
    #     pyg.click()
    # else:
    pyg.doubleClick(x=620, y=550, duration=0.5)


def passarVideo():
    time.sleep(_delayFuncao)
    pyg.click(x=1190, y=570, duration=0.5)


def voltarVideo():
    time.sleep(_delayFuncao)
    pyg.click(x=1190, y=490, duration=0.5)


def mutarVideo():
    time.sleep(_delayFuncao)
    pyg.click(x=1190, y=980, duration=0.5)


def copiarLinkVideo():
    time.sleep(_delayFuncao)
    pyg.click(x=1190, y=65, duration=0.5)
    pyg.hotkey('ctrl', 'c')
    link = pyperclip.paste()
    return link


def fecharTiktok():
    time.sleep(_delayFuncao)
    pyg.click(x=1890, y=20, duration=0.5)
