
import cv2
import numpy as np
import funcoesdb as db
import funcoespyautogui as pya
from PIL import ImageGrab

def get_frame(bbox):
    img = ImageGrab.grab(bbox)
    frame = np.array(img)
    return frame

def analyze_frames(model, list_frame, has_qtde_frame):
    has_dog = 0
    has_cat = 0
    list_conf_dog = []
    list_conf_cat = []

    for frame in list_frame:
        frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame_color)
        data_frame = results.pandas().xyxy[0]
        for index in range(len(data_frame)):
            confidence = data_frame.loc[index]['confidence']
            name = data_frame.loc[index]['name']

            if (name == 'dog' and confidence > 0.5): 
                has_dog +=1
                list_conf_dog.append(confidence)

            if (name == 'cat' and confidence > 0.5):
                has_cat +=1
                list_conf_cat.append(confidence)
    
    videoURL = pya.copiarLinkVideo()
    has_qtde_frame_dog = has_dog >= has_qtde_frame
    has_qtde_frame_cat = has_cat >= has_qtde_frame
    not_has_qtde_frame_dog = has_dog < has_qtde_frame
    not_has_qtde_frame_cat = has_cat < has_qtde_frame
    avg_conf_dog = 0
    avg_conf_cat = 0
    apareceCachorro = 1 if(has_qtde_frame_dog) else 0
    apareceGato = 1 if(has_qtde_frame_cat) else 0
    if (has_qtde_frame_dog): avg_conf_dog = round((sum(list_conf_dog)/len(list_conf_dog)),2)
    if (has_qtde_frame_cat): avg_conf_cat = round((sum(list_conf_cat)/len(list_conf_cat)),2)
    db.salvarVideo(videoURL, len(list_frame), apareceCachorro, len(list_conf_dog), avg_conf_dog, apareceGato, len(list_conf_cat), avg_conf_cat)

    if (has_qtde_frame_dog and has_qtde_frame_cat
     or has_qtde_frame_dog and not_has_qtde_frame_cat
     or has_qtde_frame_cat and not_has_qtde_frame_dog):
        pya.curtirVideo()
        return True
    return False