from keras.models import load_model
import os
import tensorflow as tf
import cv2
import numpy as np
from matplotlib import pyplot as plt

model_path = 'metal/models/newmetal.h5'
image_path = 'metal/test/'



def metal_abrasion(model_path, img_path, predictions=[]):
    model = load_model(model_path)
    for x in os.listdir(img_path):
        path = img_path + x
        img = cv2.imread(path)
        resized_img = tf.image.resize(img,(256,256))
        pred = model.predict(np.expand_dims(resized_img/255,0))
        predictions.append(pred)

    for i in range(len(predictions)):
        if predictions[i] <=0.5:
            print(f'abraised metal {i+1}')
        
    
    
def metal_inspect():
    metal_abrasion(model_path, image_path)

