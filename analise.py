
import cv2
import numpy as np
from PIL import ImageGrab
import time
import threading

class Video:

    def __init__(self, model, settings):
        self.model = model

        self.param = settings.param
        self.param_en = settings.param_en
        self.time_video_sec = settings.time_video_sec
        self.perc_video = settings.perc_video / 100
        self.crit_aceit = settings.crit_aceit / 100
        self.qt_video = settings.qt_video

        self.is_valid = 0
        self.obj_appears = 0
        self.avg_conf_obj = 0
        self.qt_frame = 0
        self.qt_frame_param = 0
        self.list_conf_obj = []
        self.list_frame = []
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

            if (name == self.param_en and confidence >= self.crit_aceit): 
                self.qt_frame_param +=1
                self.list_conf_obj.append(confidence)
                break

    def run(self):
        begin_rframe = time.perf_counter()

        first_frame = self.get_frame(bbox=(370,90,870,1020))

        sec_frame = self.get_frame(bbox=(370,90,870,1020))
        
        while(True):
            frame = self.get_frame(bbox=(370,90,870,1020))

            end_rframe = time.perf_counter()

            if (np.array_equiv(frame, first_frame) or np.array_equiv(frame, sec_frame) 
             or end_rframe - begin_rframe > self.time_video_sec): 
                self.time_video_sec = end_rframe - begin_rframe
                break

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

        for frame in self.list_frame:
            self.pred_frame(frame)
        
        self.wait_threads()

        return self.validate()

    def validate(self):

        self.qt_frame = len(self.list_frame)
        criterio_aceitacao = self.perc_video * self.qt_frame
        has_qtde_frame_obj = self.qt_frame_param >= criterio_aceitacao

        if (has_qtde_frame_obj): 
            self.obj_appears = 1
            self.avg_conf_obj = round((sum(self.list_conf_obj)/len(self.list_conf_obj)),2)
            self.is_valid = 1

        return self

# def pred_frame(model, frame):
#     frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = model(frame_color)
#     data_frame = results.pandas().xyxy[0]
#     for index in range(len(data_frame)):
#         confidence = data_frame.loc[index]['confidence']
#         name = data_frame.loc[index]['name']

#         if (name == 'dog' and confidence > 0.5):
#             global has_obj 
#             global list_conf_obj 
#             has_obj +=1
#             list_conf_obj.append(confidence)

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

#     # has_obj = 0
#     # has_cat = 0
#     # list_conf_obj = []
#     # list_conf_cat = []

#     # for frame in list_frame:
#     #     frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     #     results = model(frame_color)
#     #     data_frame = results.pandas().xyxy[0]
#     #     for index in range(len(data_frame)):
#     #         confidence = data_frame.loc[index]['confidence']
#     #         name = data_frame.loc[index]['name']

#     #         if (name == 'dog' and confidence > 0.5): 
#     #             has_obj +=1
#     #             list_conf_obj.append(confidence)

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
#     has_qtde_frame_dog = has_obj >= has_qtde_frame
#     has_qtde_frame_cat = has_cat >= has_qtde_frame
#     not_has_qtde_frame_dog = has_obj < has_qtde_frame
#     not_has_qtde_frame_cat = has_cat < has_qtde_frame
#     avg_conf_obj = 0
#     avg_conf_cat = 0
#     obj_appears = 1 if(has_qtde_frame_dog) else 0
#     apareceGato = 1 if(has_qtde_frame_cat) else 0
#     if (has_qtde_frame_dog): avg_conf_obj = round((sum(list_conf_obj)/len(list_conf_obj)),2)
#     if (has_qtde_frame_cat): avg_conf_cat = round((sum(list_conf_cat)/len(list_conf_cat)),2)
#     db.salvarVideo(videoURL, len(list_frame), obj_appears, len(list_conf_obj), avg_conf_obj, apareceGato, len(list_conf_cat), avg_conf_cat)

#     if (has_qtde_frame_dog and has_qtde_frame_cat
#      or has_qtde_frame_dog and not_has_qtde_frame_cat
#      or has_qtde_frame_cat and not_has_qtde_frame_dog):
#         pya.curtirVideo()
#         return True
#     return False