import numpy as np
import cv2 #load image
import mediapipe as mp
from detection import *

def collect_data(pose):
    folder={'war':'warrior2', 'tree':'tree', 'dd':'downward_dog'}
    function={'war':warrior2, 'tree':tree, 'dd':downward_dog}
    pose_data=""
    for i in range(1, 11):
        pose_processed=process_image(f'data/{folder[pose]}/{pose}{i}.jpg')
        landmarks=pose_processed.pose_landmarks.landmark
        line=""
        for angle in function[pose](landmarks)[1:]:
            line+=f"{angle}, "
        line+=f"{folder[pose]}\n"
        pose_data+=line
    return pose_data
     
def collect_alldata():
    with open("data_collection.csv", "w") as f: #create/overwrite a file
        f.write(collect_data('war'))
        f.write(collect_data("tree"))
        f.write(collect_data("dd"))
collect_alldata()

        
