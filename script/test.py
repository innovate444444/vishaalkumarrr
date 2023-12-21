from keras.models import load_model
import os
import tensorflow as tf
import cv2
import numpy as np
from matplotlib import pyplot as plt




def crack_detection(model_path,img_path,predictions=[]):
    model = load_model(model_path)
    images_with_cracks = []
    for x in os.listdir(img_path):
        path = img_path + x
        img = cv2.imread(path)
        resized_img = tf.image.resize(img,(256,256))
        pred = model.predict(np.expand_dims(resized_img/255,0))
        if pred >= 0.5:
            images_with_cracks.append(path)
            #the path is only relative path
        predictions.append(pred)

    #for i in images_with_cracks:
    #    print(i)

    return images_with_cracks

# model_path = 'CNN/models/imageclassifier.h5'
# image_path = 'enhancement/output/images/'

# l1 = crack_detection(model_path, image_path)
# for i in l1:
#    print(i)


