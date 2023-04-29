
import torch
import cv2
import numpy as np
from PIL import Image
import os
import re

# Carrego o modelo pré treinado - YOLO
tipo_modelo = 'yolov5x' # yolov5n, yolov5s, yolov5m, yolov5l, yolov5x  -- Coloquei em ordem qual modelo esta mais treinado
usa_cuda = torch.cuda.is_available()
dispositivo = torch.device("cuda" if usa_cuda else "cpu")
modelo = torch.hub.load('ultralytics/yolov5', tipo_modelo, dispositivo)

# Defino o caminho das imagens de cachorro
dir_atual = os.path.abspath(os.path.dirname(__file__))
pasta_imagens = os.path.join(dir_atual, "img", "criterio_aceitacao")

# Defino a expressão regular para separar o nome do arquivo em prefixo e número
regex = r"(\D+)(\d+)"

# Listo os arquivos na pasta de imagens e ordeno pelo número
arquivos = sorted(os.listdir(pasta_imagens), key=lambda x: int(re.split(regex, x)[2]))

# Defino a função que vai fazer a predição das imagens 
def predicao(modelo, imagem):
    resultados = modelo(imagem)
    data_frame = resultados.pandas().xyxy[0]
    for index in range(len(data_frame)):
        name = data_frame.loc[index]['name']
        escore = data_frame.loc[index]['confidence']
        print(str(name) + ' - ' + str(escore))

print('Imagens')
# Imprime o nome de cada arquivo
print('----------')
for arquivo in arquivos:
    print(arquivo)
    imagem = Image.open(os.path.join(pasta_imagens, arquivo))
    predicao(modelo, imagem)
    print('----------')


