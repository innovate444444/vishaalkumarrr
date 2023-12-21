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
	cv2.imshow('image1',output_img)
	cv2.imshow('image2',img)
	cv2.waitKey(0)
	cv2.imwrite('static/images/rust/output_image%d.jpg'%count,output_img)
	rust[key_name].append(f"static/images/rust/output_image{count}.jpg")
	cv2.imwrite('static/images/rust/image%d.jpg'%count,img)
	rust[key_name].append(f"static/images/rust/image{count}.jpg")
	cv2.destroyAllWindows()
	os.system("cls")
	
	
	
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

	input("\n PRESS ENTER TO EXIT ")

corrosion()
print(rust)

