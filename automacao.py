import funcoespyautogui as pya
import funcoesanalise as ma
import funcoesdb as db
import torch
#from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import ImageGrab
import time
import pyautogui
import os
import multiprocessing as mp
from itertools import repeat

print("*************************************************")
print("Quanto tempo a ferramenta vai ficar executando em minutos:", end = ' ')
min = int(input())
sec = min * 60

print("*************************************************")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
print("*************************************************")
print("MODELO CARREGADO")

pya.abrirTiktok()
time.sleep(10)
pya.abrirMidia()
time.sleep(2)

print("*************************************************")
print("MIDIA CARREGADA")

begin_tool = time.perf_counter()
end_tool = time.perf_counter()
videos = 0
while(sec > end_tool - begin_tool):

    pya.passarVideo()
    time.sleep(2)

    list_frame = []
    list_results = []

    first_frame = ma.get_frame(bbox=(370,130,870,1020))
    list_frame.append(first_frame)

    sec_frame = ma.get_frame(bbox=(370,130,870,1020))
    list_frame.append(sec_frame)

    loop_time = time.time()

    begin_rframe = time.perf_counter()
    while(True):

        # Vejo 20 segundos de frame, coloquei 22 para descontar os 2 segundos de espera ao passar de video
        frame = ma.get_frame(bbox=(370,130,870,1020))
        end_rframe = time.perf_counter()
        if ((np.array_equiv(frame, first_frame) or np.array_equiv(frame, sec_frame)) or end_rframe - begin_rframe > 22): break
        else: list_frame.append(frame)

        # # Cria tela com a analise dos frames
        # frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # results = model(frame_color)
        # imS = cv2.resize(np.squeeze(results.render()), (300, 400))
        # #imS2 = cv2.resize(frame, (300, 400))
        # cv2.imshow('YOLO', imS)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #    break
        # cv2.destroyAllWindows()

        # # Frames por segundo
        # print('FPS {}'.format(1 / (time.time() - loop_time)))
        # loop_time = time.time()
        
        # # Tempo de Execução
        # total = round(end - begin, 2)
        # print(f'Runtime: {total}')


    # Aproximadamente 420 frames em 21 segundos 
    # Então, 20 frames por segundo
    # Video tem que ter no minimo 2 segundos relacionado aquele conteudo de animal
    # Logo, 20x2 = 40 frames com aquele conteudo

    has_animal = ma.analyze_frames(model, list_frame, 40)
    if (has_animal): time.sleep(3)

    end_tool = time.perf_counter()
    videos += 1
    
print("*************************************************")
print(f'Videos analisados: {videos}')
pya.fecharMidia()
db.fecharConexao()
