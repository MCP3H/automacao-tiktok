import cv2
import numpy as np
from PIL import ImageGrab
import time
import torch

# Carrego o modelo pré treinado - YOLO
tipo_modelo = 'yolov5x' # yolov5n, yolov5s, yolov5m, yolov5l, yolov5x  -- Coloquei em ordem qual modelo esta mais treinado
usa_cuda = torch.cuda.is_available()
dispositivo = torch.device("cuda" if usa_cuda else "cpu")
modelo = torch.hub.load('ultralytics/yolov5', tipo_modelo, dispositivo)

# Defino a função que vai pegar os frames da tela
def pega_imagem(bbox):
    img = ImageGrab.grab(bbox)
    frame = np.array(img)
    return frame

loop_time = time.time()
# Looping para reconhecer a iamgem 
while(True):
    frame = pega_imagem(bbox=(370,90,870,1020))

    # Cria tela com a analise dos frames
    frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = modelo(frame_color)
    imS = cv2.resize(np.squeeze(results.render()), (300, 400))
    # imS2 = cv2.resize(frame, (300, 400))
    cv2.imshow('YOLO', imS)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    # Frames por segundo
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()
