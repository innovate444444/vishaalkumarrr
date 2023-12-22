#process:
#video -> frame extraction -> enhancement -> model



#app part :as app.py can be the only that runs all the backend process in one and we want to display the images from here ,we are placing all the function in here



import cv2
import os

#frames extraction parameters (video_file_path, output_frames_folder, optional_frame_interval(60))
from script.video import extract_frames
def frame_extraction():
    video_parent_dir = 'video/'
    output_frames_folder = 'frames'
    optional_frame_interval = 30
    x = os.listdir(video_parent_dir)
    video_file_path = video_parent_dir + x[0]

    extract_frames(video_file_path, output_frames_folder, optional_frame_interval)
    print("\n\nEXTRACTION OF FRAMES COMPLETED SUCCESSFULLY\n\n")

#enhancement paramenters (script_path, input_file_path, output_file_fath)
import subprocess


def enhancement():
    script_path = 'enhancement/finalEnhancer.py'
    input_file_path = 'frames'
    output_file_path = 'images'
    weights = 'enhancement/weights.pt'

    command = [
    'python', script_path,
    '--source', input_file_path,
    '--name', output_file_path,
    '--weights', weights
]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Command output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Command output (if available):", e.output)

    print("ENHANCEMENT OF IMAGES COMPLETED SUCCESSFULLY")



from script.test import crack_detection
#crack detection model parameters (model_path, imgs_path)
def crack_processing():

    model_path = 'CNN/models/newmodel.h5'
    image_path = 'enhancement/output/images/'  
    #include '/' at the end of image path sd os.listdir() does not

    crack_detected_image_paths = crack_detection(model_path, image_path)
    #print(crack_detected_image_paths)
    return crack_detected_image_paths
from keras.models import load_model
import os
import tensorflow as tf
import cv2
import numpy as np
from matplotlib import pyplot as plt

model_path = 'metal/models/newmetal.h5'
image_path = 'metal/test/'



def metal_abrasion_detection(model_path,img_path,predictions=[]):
    model = load_model(model_path)
    images_with_abrasions= []
    for x in os.listdir(img_path):
        path = img_path + x
        img = cv2.imread(path)
        resized_img = tf.image.resize(img,(256,256))
        pred = model.predict(np.expand_dims(resized_img/255,0))
        if pred >= 0.5:
            images_with_abrasions.append(path)
            #the path is only relative path
        predictions.append(pred)

    #for i in images_with_cracks:
    #    print(i)

    return images_with_abrasions
        
    
    
def metal_inspect():
    abrasions=metal_abrasion_detection(model_path, image_path)
    return abrasions



import cv2
from sys import argv
import numpy as np
import os
import glob

count = 0

rust = {}
i=1

def rust_detect(file):
	
			
           
	global i
	img = cv2.imread(file)
	img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	# Range for lower red
	lower_red = np.array([0,70,70])
	upper_red = np.array([20,200,150])
	mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
	
	# range for upper red
	lower_red = np.array([170,70,70])
	upper_red = np.array([180,200,150])
	mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
	
	# add both masks
	mask = mask0+mask1
	
	output_img = cv2.bitwise_and(img,img,mask=mask)
    
	pixels = (np.sum(mask)/255)
	print("\n\n\n Number of pixels depicting rust \n >> %d"%pixels)
	key_name = f"frame{i}"
	if key_name not in rust:
		rust[key_name] = []
	
	rust[key_name].append(pixels)
	

	def defuzzification(pixel):
		
		
	
		if(pixel == 0):
			print("NO CORROSION")
			rust[key_name].append("NO CORROSION")
			
		elif(pixel <100000 and pixel > 0):
			print("LOW CORROSION")
			rust[key_name].append("LOW CORROSION")
			
		elif(pixel<200000 and pixel >= 100000):
			rust[key_name].append("FAIRLY LOW CORROSION")
			print("FAIRLY LOW CORROSION")
		
			print("FAIRLY LOW CORROSION")
		elif(pixel <300000 and pixel >= 300000):
			rust[key_name].append("MEDIUM CORROSION")
			print("MEDIUM CORROSION")
		elif(pixel <400000 and pixel >= 300000):
			print("FAIRLY HIGH CORROSION")
			rust[key_name].append("FAIRLY HIGH CORROSION")
		elif(pixel >= 400000):
			print("VERY high CORROSION")
			rust[key_name].append("VERY high CORROSION")
			
	defuzzification(pixels)
	output_img = cv2.resize(output_img, (500,500))
	img = cv2.resize(img, (500,500))    
	
	cv2.imwrite('static/images/rust/output_image%d.jpg'%count,output_img)
	rust[key_name].append(f"static/images/rust/output_image{count}.jpg")
	cv2.imwrite('static/images/rust/image%d.jpg'%count,img)
	rust[key_name].append(f"static/images/rust/image{count}.jpg")
	
	
	
	
	
os.system("color 0a")
os.system("cls")

#update image folder path "ADD / IN THE END"
image_folder = 'enhancement/output/images/'
imgs = os.listdir(image_folder)

def corrosion():
	global count
	global i
	
	for x in imgs:
		
		count+=1
		img_path = image_folder + x
		print(img_path)
		rust_detect(img_path)
		i+=1

rust = {}

def corrosionx():
    global rust

    # Check if results are already available
    if not rust:
        corrosion()

    return rust



# frame_extraction()
# enhancement()
# crack_processing()
