
import cv2
import numpy as np
from PIL import ImageGrab
import time
import threading

class Video:

    def __init__(self, model, sec_video):
        self.model = model
        self.sec_video = sec_video
        self.has_animal = False
        self.apareceCachorro = 0
        self.apareceGato = 0
        self.avg_conf_dog = 0
        self.avg_conf_cat = 0
        self.has_dog = 0
        self.has_cat = 0
        self.list_frame = []
        self.list_conf_dog = []
        self.list_conf_cat = []
        self.list_threads = []

    def get_frame(self, bbox):
        img = ImageGrab.grab(bbox)
        frame = np.array(img)
        self.list_frame.append(frame)
        return frame
    
    def pred_frame(self, frame):
        t = threading.Thread(target=self.prediction, args=[frame])
        self.list_threads.append(t)
        t.start()

    def wait_threads(self):
        for thread in self.list_threads:
            thread.join()
    
    def prediction(self, frame):
        frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(frame_color)
        data_frame = results.pandas().xyxy[0]
        for index in range(len(data_frame)):
            confidence = data_frame.loc[index]['confidence']
            name = data_frame.loc[index]['name']

            if (name == 'dog' and confidence >= 0.5): 
                self.has_dog +=1
                self.list_conf_dog.append(confidence)

            if (name == 'cat' and confidence >= 0.5):
                self.has_cat +=1
                self.list_conf_cat.append(confidence) 

    def run(self):

        begin_rframe = time.perf_counter()

        first_frame = self.get_frame(bbox=(370,130,870,1020))
        #self.pred_frame(first_frame)

        sec_frame = self.get_frame(bbox=(370,130,870,1020))
        #self.pred_frame(sec_frame)
        
        while(True):
            frame = self.get_frame(bbox=(370,130,870,1020))
            #self.pred_frame(sec_frame)
            end_rframe = time.perf_counter()

            if (np.array_equiv(frame, first_frame) or np.array_equiv(frame, sec_frame) 
             or end_rframe - begin_rframe > self.sec_video): 
                self.sec_video = end_rframe - begin_rframe
                break

        ## frames ta estranho, ele capta que tem cachorro, mas ta salvando vazio no banco por algum motivo 
        for frame in self.list_frame:
            self.pred_frame(frame)

            # # Cria tela com a analise dos frames
            # frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # results = self.model(frame_color)
            # imS = cv2.resize(np.squeeze(results.render()), (300, 400))
            # #imS2 = cv2.resize(frame, (300, 400))
            # cv2.imshow('YOLO', imS)
            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #    break

            # # Frames por segundo
            # print('FPS {}'.format(1 / (time.time() - loop_time)))
            # loop_time = time.time()
            
            # # Tempo de Execução
            # total = round(end - begin, 2)
            # print(f'Runtime: {total}')

        self.wait_threads()
        return self.validate()

    def validate(self):

        # Regra: O video precisa ter pelo menos 2 segundos de cachorro/gato para o conteudo ser de animal domestico
        # Se em aproximadamente 20 segundos, for pego 420 frames
        # Então, são 21 frames por segundos
        # Logo, para o critério de aceitação o conteudo de animal domestico precisa ter 21x2 = 42 frames

        qtde_frames = len(self.list_frame)
        fps = qtde_frames/self.sec_video
        criterio_aceitacao = fps * 2

        has_qtde_frame_dog = self.has_dog >= criterio_aceitacao
        has_qtde_frame_cat = self.has_cat >= criterio_aceitacao

        if (has_qtde_frame_dog): 
            self.apareceCachorro = 1
            self.avg_conf_dog = round((sum(self.list_conf_dog)/len(self.list_conf_dog)),2)

        if (has_qtde_frame_cat): 
            self.apareceGato = 1
            self.avg_conf_cat = round((sum(self.list_conf_cat)/len(self.list_conf_cat)),2)

        if (has_qtde_frame_dog and has_qtde_frame_cat
        or has_qtde_frame_dog and not has_qtde_frame_cat
        or has_qtde_frame_cat and not has_qtde_frame_dog):
            self.has_animal = True
        
        return self

# def pred_frame(model, frame):
#     frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = model(frame_color)
#     data_frame = results.pandas().xyxy[0]
#     for index in range(len(data_frame)):
#         confidence = data_frame.loc[index]['confidence']
#         name = data_frame.loc[index]['name']

#         if (name == 'dog' and confidence > 0.5):
#             global has_dog 
#             global list_conf_dog 
#             has_dog +=1
#             list_conf_dog.append(confidence)

#         if (name == 'cat' and confidence > 0.5):
#             global has_cat 
#             global list_conf_cat
#             has_cat +=1
#             list_conf_cat.append(confidence)

# async def loop_frames(loop, model, list_frame):
#     list_task = []
#     for frame in list_frame:
#         task = loop.create_task(pred_frame(model, frame))
#         list_task.append(task)
#     await asyncio.wait(list_task)

# def analyze_frames(model, list_frame, has_qtde_frame):

#     # begin = time.perf_counter()

#     # with concurrent.futures.ThreadPoolExecutor() as executor:
#     #     executor.map(pred_frame, repeat(model), list_frame)

#     # # # Tempo de Execução
#     # end = time.perf_counter()
#     # total = round(end - begin, 2)
#     # print(f'Runtime: {total}')

#     # ********************************************************************

#     # begin = time.perf_counter()

#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(loop_frames(loop, model, list_frame))

#     # # # Tempo de Execução
#     # end = time.perf_counter()
#     # total = round(end - begin, 2)
#     # print(f'Runtime: {total}')

#     # ********************************************************************

#     # begin = time.perf_counter()

#     # has_dog = 0
#     # has_cat = 0
#     # list_conf_dog = []
#     # list_conf_cat = []

#     # for frame in list_frame:
#     #     frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     #     results = model(frame_color)
#     #     data_frame = results.pandas().xyxy[0]
#     #     for index in range(len(data_frame)):
#     #         confidence = data_frame.loc[index]['confidence']
#     #         name = data_frame.loc[index]['name']

#     #         if (name == 'dog' and confidence > 0.5): 
#     #             has_dog +=1
#     #             list_conf_dog.append(confidence)

#     #         if (name == 'cat' and confidence > 0.5):
#     #             has_cat +=1
#     #             list_conf_cat.append(confidence)
    
#     # # # Tempo de Execução
#     # end = time.perf_counter()
#     # total = round(end - begin, 2)
#     # print(f'Runtime: {total}')

#     # ********************************************************************
    
#     print(f'Quantidades de frames: {len(list_frame)}')
#     videoURL = pya.copiarLinkVideo()
#     has_qtde_frame_dog = has_dog >= has_qtde_frame
#     has_qtde_frame_cat = has_cat >= has_qtde_frame
#     not_has_qtde_frame_dog = has_dog < has_qtde_frame
#     not_has_qtde_frame_cat = has_cat < has_qtde_frame
#     avg_conf_dog = 0
#     avg_conf_cat = 0
#     apareceCachorro = 1 if(has_qtde_frame_dog) else 0
#     apareceGato = 1 if(has_qtde_frame_cat) else 0
#     if (has_qtde_frame_dog): avg_conf_dog = round((sum(list_conf_dog)/len(list_conf_dog)),2)
#     if (has_qtde_frame_cat): avg_conf_cat = round((sum(list_conf_cat)/len(list_conf_cat)),2)
#     db.salvarVideo(videoURL, len(list_frame), apareceCachorro, len(list_conf_dog), avg_conf_dog, apareceGato, len(list_conf_cat), avg_conf_cat)

#     if (has_qtde_frame_dog and has_qtde_frame_cat
#      or has_qtde_frame_dog and not_has_qtde_frame_cat
#      or has_qtde_frame_cat and not_has_qtde_frame_dog):
#         pya.curtirVideo()
#         return True
#     return False