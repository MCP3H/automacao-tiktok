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
    settings.param = model.names[settings.chave]

    print("*************************************************")
    print("Quanto tempo de frame vai ser analisado dos vídeos (em segundos/video completo(0)):", end=" ")
    settings.time_video_sec = int(input())

    print("*************************************************")
    print("Qual o percentual de frames que o objeto(" + settings.param + ") tem que aparecer no vídeo (0 a 100):", end=" ")
    settings.perc_video = int(input())

    print("*************************************************")
    print("Tempo de execução(0) ou quantidade de vídeos(1):", end=" ")
    settings.type_exe = int(input())

    settings.time_exec_min = 0
    settings.sec = 0
    settings.qt_video = 0
    if(settings.type_exe == 0):
        print("*************************************************")
        print("Quanto tempo a ferramenta vai ficar executando (em minutos):", end=" ")
        settings.time_exec_min = int(input())
        settings.sec = settings.time_exec_min * 60
    elif(settings.type_exe == 1):
        print("*************************************************")
        print("Quantos vídeos vc deseja captar:", end=" ")
        settings.qt_video = int(input())

    config = db.createConfig(settings)
    
    # MIDIA

    print("*************************************************")
    print("ABRINDO MIDIA")
    pya.openTiktok()
    time.sleep(10)
    pya.searchVideo(settings.param)
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

    while((settings.sec > end_tool - begin_tool) or (settings.qt_video > videos)):
        
        video = ma.Video(model, settings)

        # Find video
        while(True):
            video_url = pya.copyLinkVideo()
            video_url = video_url.split("?q=")[0]
            has_video = db.listarVideosURL(video_url)
            if len(has_video) > 0:
                pya.passVideo()
            else:
                break
        
        time.sleep(1)
        analise = video.run()
        if (analise.is_valid):
            pya.likeVideo()
            videos += 1

        db.salvarVideo(config, video_url, analise.qt_frame, analise.qt_frame_param, analise.is_valid)

        videos_ana += 1

        pya.passVideo()
        time.sleep(1)

        end_tool = time.perf_counter()
        
    print("*************************************************")
    print(f'Videos analisados: {videos_ana}')

    pya.closeVideo()
    db.fecharConexao()
