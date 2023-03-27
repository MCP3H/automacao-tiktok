import funcoespyautogui as pya
import funcoesanalise as ma
import funcoesdb as db
import torch
import time

if __name__ == '__main__':

    print("*************************************************")
    print("YOLOV5 - Gerador de base de vídeos para treinamento de IA")

    # MODELO

    print("*************************************************")
    print("CARREGANDO O MODELO")
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device)
    print("*************************************************")
    print("MODELO CARREGADO")
    
    # PARAMS

    class Settings(object):
        pass
    settings = Settings()

    print("*************************************************")
    print("Em relação a esses objetos:")
    print("*")
    for key, value in model.names.items():
        print(str(key) + ": " + value)
    print("*")
    print("Digita a chave do que vai ser detectado nos vídeos:", end=" ")
    settings.chave = int(input())
    settings.chave_name = model.names[settings.chave]

    print("*************************************************")
    print("Quanto tempo de frame vai ser analisado dos vídeos (em segundos/video completo(0)):", end=" ")
    settings.sec_video = int(input())

    print("*************************************************")
    print("Qual o percentual de frames que o objeto(" + settings.chave_name + ") tem que aparecer no vídeo (0 a 100):", end=" ")
    settings.perc = int(input()) / 100

    print("*************************************************")
    print("Tempo de execução(0) ou quantidade de vídeos(1):", end=" ")
    settings.type_exe = int(input())

    settings.min = 0
    settings.sec = 0
    settings.qtde_video = 0
    if(settings.type_exe == 0):
        print("*************************************************")
        print("Quanto tempo a ferramenta vai ficar executando (em minutos):", end=" ")
        settings.min = int(input())
        settings.sec = settings.min * 60
    elif(settings.type_exe == 1):
        print("*************************************************")
        print("Quantos vídeos vc deseja captar:", end=" ")
        settings.qtde_video = int(input())

    video = ma.Video(model, settings)
    
    # MIDIA

    print("*************************************************")
    print("ABRINDO MIDIA")
    pya.openTiktok()
    time.sleep(10)
    pya.searchVideo(settings.chave_name)
    time.sleep(2)
    pya.openVideo()
    time.sleep(1)
    print("*************************************************")
    print("MIDIA CARREGADA")

    # ANALISE

    begin_tool = time.perf_counter()
    end_tool = time.perf_counter()
    videos = 0
    videos_ana = 0

    while((settings.sec > end_tool - begin_tool) or (settings.qtde_video > videos)):
        
        # Find video
        while(True):
            videoURL = pya.copyLinkVideo()
            videoURL = videoURL.split("?q=")[0]
            has_video = db.listarVideosURL(videoURL)
            if len(has_video) > 0:
                pya.passVideo()
            else:
                break
        
        time.sleep(1)
        analise = video.run()
        if (analise.has_obj):
            pya.likeVideo()
            db.salvarVideo(videoURL)
            videos += 1

        videos_ana += 1

        pya.passVideo()
        time.sleep(1)

        end_tool = time.perf_counter()
        
    print("*************************************************")
    print(f'Videos analisados: {videos_ana}')

    pya.closeVideo()
    db.fecharConexao()
