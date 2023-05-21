
import cv2
import numpy as np
from PIL import ImageGrab
import time
import threading
import torch
from multiprocessing import Process

class Video:

    def __init__(self, model, settings):
        self.model = model

        self.param = settings.param
        self.param_en = settings.param_en
        self.time_video_sec = settings.time_video_sec
        self.perc_video = settings.perc_video / 100
        self.crit_aceit = settings.crit_aceit / 100
        self.qt_video = settings.qt_video
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.is_valid = 0
        self.obj_appears = 0
        self.avg_conf_obj = 0
        self.qt_frame = 0
        self.qt_frame_param = 0
        self.list_conf_obj = []
        self.list_frame = []
        # self.list_threads = []

    def get_frame(self, bbox):
        img = ImageGrab.grab(bbox)
        frame = np.array(img)
        self.list_frame.append(frame)
        return frame
    
    # def pred_frame(self, frame):
    #     t = threading.Thread(target=self.prediction, args=[frame])
    #     self.list_threads.append(t)
    #     t.start()

    # def wait_threads(self):
    #     for thread in self.list_threads:
    #         thread.join()
    
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

        for frame in self.list_frame:
            self.prediction(frame)

        # for frame in self.list_frame:
        #     self.pred_frame(frame)
        
        # self.wait_threads()
        #     self.prediction(frame)

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
    