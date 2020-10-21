import pickle
from PIL import Image
import cv2 #opencv
import io
import numpy as np
from io import BytesIO
import base64
from Config import *
import os
import pandas as pd
from collections import deque

def save_obj(obj, name ):
    with open('objects/'+ name + '.pkl', 'wb') as f: #dump files into objects folder
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name ):
    with open('objects/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def grab_screen(_driver):
    image_b64 = _driver.execute_script(getbase64Script)
    screen = np.array(Image.open(BytesIO(base64.b64decode(image_b64))))
    image = process_img(screen)#processing image as required
    # print("2", image.shape)
    return image

def process_img(image):
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #RGB to Grey Scale
    image = image[:300, :500] #Crop Region of Interest(ROI)
    # print("1", image.shape)
    image = cv2.resize(image, (80,80))
    return  image

def show_img(graphs = False):
    """
    Show images in new window
    """
    while True:
        screen = (yield)
        window_title = "logs" if graphs else "game_play"
        cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)        
        imS = cv2.resize(screen, (800, 400)) 
        cv2.imshow(window_title, screen)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break


#Intialize log structures from file if exists else create new
loss_df = pd.read_csv(loss_file_path) if os.path.isfile(loss_file_path) else pd.DataFrame(columns =['loss']).to_csv(loss_file_path)
scores_df = pd.read_csv(scores_file_path) if os.path.isfile(scores_file_path) else pd.DataFrame(columns = ['scores']).to_csv(scores_file_path)
actions_df = pd.read_csv(actions_file_path) if os.path.isfile(actions_file_path) else pd.DataFrame(columns = ['actions']).to_csv(actions_file_path)
q_values_df =pd.read_csv(actions_file_path) if os.path.isfile(q_value_file_path) else pd.DataFrame(columns = ['qvalues']).to_csv(q_value_file_path)

# training variables saved as checkpoints to filesystem to resume training from the same step
def init_cache():
    """initial variable caching, done only once"""
    save_obj(INITIAL_EPSILON,"epsilon")
    t = 0
    save_obj(t,"time")
    D = deque()
    save_obj(D,"D")