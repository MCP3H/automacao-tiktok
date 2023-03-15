import funcoespyautogui as pya
import funcoesanalise as ma
import funcoesdb as db
import torch
import time

if __name__ == '__main__':

    print("*************************************************")
    print("Tempo de execução da ferramenta (em minutos):", end = ' ')
    min = int(input())
    sec = min * 60

    print("Tempo de espera para captar os frames após passar de video (em segundos):", end = ' ')
    delay = int(input())

    print("Tempo de análise de frames dos videos (em segundos):", end = ' ')
    sec_video = int(input()) + delay

    print("*************************************************")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.share_memory()
    print("*************************************************")
    print("MODELO CARREGADO")
    
    pya.abrirTiktok()
    time.sleep(10)
    pya.abrirMidia()
    time.sleep(delay)

    print("*************************************************")
    print("MIDIA CARREGADA")

    begin_tool = time.perf_counter()
    end_tool = time.perf_counter()
    videos = 0
    while(sec > end_tool - begin_tool):

        video = ma.Video(model, sec_video)

        analise = video.run()

        if (analise.has_animal): 
            pya.curtirVideo()
            time.sleep(3)
        
        videoURL = pya.copiarLinkVideo()
        db.salvarVideo(videoURL, len(analise.list_frame), 
                       analise.apareceCachorro, len(analise.list_conf_dog), analise.avg_conf_dog, 
                       analise.apareceGato, len(analise.list_conf_cat), analise.avg_conf_cat)

        videos += 1

        pya.passarVideo()
        time.sleep(delay)

        end_tool = time.perf_counter()
        
    print("*************************************************")
    print(f'Videos analisados: {videos}')

    pya.fecharMidia()
    db.fecharConexao()
