import automacao as pya
import analise as ma
import banco as db
import torch
import time
from app import app

if __name__ == '__main__':

    print("*************************************************")
    print("YOLOV5 - Gerador de base de vídeos para treinamento de IA")

    # MODELO

    print("*************************************************")
    print("CARREGANDO O MODELO")
    tipo_modelo = 'yolov5x' # yolov5n, yolov5s, yolov5m, yolov5l, yolov5x  -- Coloquei em ordem qual modelo esta mais treinado
    usa_cuda = torch.cuda.is_available()
    dispositivo = torch.device("cuda" if usa_cuda else "cpu")
    modelo = torch.hub.load('ultralytics/yolov5', tipo_modelo, dispositivo)
    print("*************************************************")
    print("MODELO CARREGADO")
    
    # PARAMS

    class Settings(object):
        pass
    settings = Settings()
    settings.modelo = tipo_modelo

    print("*************************************************")
    print("Em relação a esses objetos:")
    print("*")
    for key, value in modelo.names.items():
        print(str(key) + ": " + value)
    print("*")
    print("Digita a chave do objeto que vai ser detectado nos vídeos:", end=" ")
    settings.chave = int(input())
    settings.param = modelo.names[settings.chave]

    print("*************************************************")
    print("Qual o percentual de critério de aceitação dos frames (0 a 100):", end=" ")
    settings.crit_aceit = int(input())

    print("*************************************************")
    print("Quanto tempo de frame vai ser analisado dos vídeos (em segundos):", end=" ")
    settings.time_video_sec = int(input())

    print("*************************************************")
    print("Qual o percentual de frames que o objeto tem que aparecer no vídeo (0 a 100):", end=" ")
    settings.perc_video = int(input())

    print("*************************************************")
    print("Quantos vídeos vc deseja analisar:", end=" ")
    settings.qt_video = int(input())

    conexao = db.abrirConexao()
    config = db.criarParametro(conexao, settings)
    
    # MIDIA

    print("*************************************************")
    print("ABRINDO MIDIA")
    pya.abrirTiktokTag(settings.param)
    time.sleep(10)
    pya.abrirMidia()
    time.sleep(1)
    print("*************************************************")
    print("MIDIA CARREGADA")

    # ANALISE
    videos = 0
    videos_ana = 0
    begin_tool = time.perf_counter()
    end_tool = time.perf_counter()
    while(settings.qt_video > videos_ana):
        
        video = ma.Video(modelo, settings)

        # Find video
        while(True):
            video_url = pya.copiarLinkVideo()
            video_url = video_url.split("?q=")[0]
            has_video = db.verificarVideo(conexao, video_url, config)
            if len(has_video) > 0:
                pya.passarVideo()
            else:
                break
        
        time.sleep(1)

        analise = video.run()
        if (analise.is_valid):
            videos += 1

        db.salvarVideo(conexao, config, video_url, analise.qt_frame, analise.qt_frame_param, analise.is_valid)

        videos_ana += 1

        pya.passarVideo()
        time.sleep(1)

        end_tool = time.perf_counter()
        
    print("*************************************************")
    print(f'Videos analisados: {videos_ana}')
    print(f'Videos analisados passou no param: {videos}')
    print(f'Tempo de execucao: {end_tool - begin_tool}')

    pya.fecharMidia()
    db.fecharConexao(conexao)
    pya.abrirLocalhost()
    app.run()
