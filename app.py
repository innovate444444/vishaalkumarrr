# from flask import Flask, render_template,request,jsonify
# # from script.test import crack_detection
# import cv2
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
    
#     return render_template('display_images.html')

# @app.route('/saveVideo', methods=['POST'])
# def save_video():
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video found'}), 400
    
#     video = request.files['video']
#     video.save('video/recorded_video.webm')
#     video.save('history/recorded_video.webm')
    
#     return jsonify({'message': 'File saved successfully'}), 200

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# import os
# import uuid  # Python library for generating unique IDs
# from script.video import extract_frames
# import cv2
# import opencv

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('display_images.html')

# @app.route('/saveVideo', methods=['POST'])
# def save_video():
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video found'}), 400
    
#     video = request.files['video']
    
#     # Generate a unique filename for the history directory
#     unique_filename = str(uuid.uuid4()) + '.webm'

#     history_path = os.path.join('history', unique_filename)
#     video.save(history_path)

#     # Replace the existing file in the video directory with the new one
#     video_path ='video/recorded_video.webm'

#     if os.path.exists(video_path):
#         os.remove(video_path)
#     video.save(video_path)

#     # video_file_path = 'video/recorded_video.webm'

#     # output_frames_folder = 'raw_imgs'
#     # frame_interval = 30  # Change this value to save every 100th or 200th frame
#     # extract_frames(video_file_path, output_frames_folder, frame_interval)


#     return jsonify({'message': 'File saved successfully'}), 200

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify,render_template, request, jsonify
import os
import uuid
import cv2
import shutil
import os

import backend
import json

app = Flask(__name__)

# # Define paths to the folders
# source_folder = 'enhancement/output/images/'
# destination_folder = 'static/output/images/'

# def move_images():
#             moved_image_paths = []  # List to store moved image paths
# # Ensure the destination folder exists, create it if it doesn't
#             os.makedirs(destination_folder, exist_ok=True)

#     # Get a list of image files in the source folder
#             image_files = os.listdir(source_folder)

#     # Move each image file to the destination folder and collect paths
#             for file_name in image_files:
#                 source_path = os.path.join(source_folder, file_name)
#                 destination_path = os.path.join(destination_folder, file_name)
#                 shutil.move(source_path, destination_path)
#                 moved_image_paths.append(destination_path.replace('static', ''))  # Adjust path for usage in the frontend
#                 return moved_image_paths

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/crack')
def crack():
    return render_template('crackdetection.html')

@app.route('/abrasion')
def abrasion():
    return render_template('abrasion.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/rust')
def rust_result():
    global rust_result
    rust_result = None

    # Check if rust result is not already computed
    if rust_result is None:
        rust_result = backend.corrosionx()
        print(rust_result)

    return render_template('rust.html', rust=rust_result)
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        file_path = 'video/recorded_video.webm'  # Define the file path to replace

        # Delete the existing file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Save the new uploaded file
        file.save(file_path)

        import backend    
        backend.frame_extraction()

        backend.enhancement()
        
       
        detected_cracks=backend.crack_processing()
        # print(detected_cracks)
        # detected_cracks=move_images(detected_cracks)
        # moved_paths = move_images()
        # print(moved_paths)
        rust=backend.corrosionx()
        print(rust)

        output_folder = 'static/images/crack'

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        saved_image_paths = []

        for index, image_path in enumerate(detected_cracks):
            # Read the image
            img = cv2.imread(image_path)

            # Process the image if needed

            # Extract the file name and extension from the path
            file_name = "crack_image.jpg"  # Initial file name
            base_name, extension = os.path.splitext(file_name)
            index=0
            # Check if the file already exists
            while os.path.exists(os.path.join(output_folder, file_name)):
                index += 1
                file_name = f"{base_name}_{index}{extension}"

            # Specify the output path for the image in the output folder
            output_path = os.path.join(output_folder, file_name)

            # Save the image to the output folder
            cv2.imwrite(output_path, img)

            # Save the path of the saved image
            saved_image_paths.append(output_path)



        # print(detected_cracks)

        saved_image_paths = [path.replace('\\', '/') for path in saved_image_paths]

        print(saved_image_paths)

        metal_abrasions=backend.metal_inspect()
        output_folder = 'static/images/metal'

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        saved_image_path = []

        for index, image_path in enumerate(metal_abrasions):
            # Read the image
            img = cv2.imread(image_path)

            # Process the image if needed

            # Extract the file name and extension from the path
            file_name = "metal_image.jpg"  # Initial file name
            base_name, extension = os.path.splitext(file_name)
            index=0
            # Check if the file already exists
            while os.path.exists(os.path.join(output_folder, file_name)):
                index += 1
                file_name = f"{base_name}_{index}{extension}"

            # Specify the output path for the image in the output folder
            output_path = os.path.join(output_folder, file_name)

            # Save the image to the output folder
            cv2.imwrite(output_path, img)

            # Save the path of the saved image
            saved_image_path.append(output_path)



        # print(detected_cracks)

        saved_image_path = [path.replace('\\', '/') for path in saved_image_paths]

        print(saved_image_path)


        return render_template('home.html', saved_image_path=saved_image_path)

        
def clear_folder(folder_path):

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    
# source_folder = 'enhancement/output/images/'
# destination_folder = 'static/output/images/'
# def move_images():
#     moved_image_paths = []  # List to store moved image paths

#     # Ensure the destination folder exists, create it if it doesn't
#     os.makedirs(destination_folder, exist_ok=True)

#     # Get a list of image files in the source folder
#     image_files = os.listdir(source_folder)

#     # Move each image file to the destination folder and collect paths
#     for file_name in image_files:
#         source_path = os.path.join(source_folder, file_name)
#         destination_path = os.path.join(destination_folder, file_name)
#         shutil.move(source_path, destination_path)
#         moved_image_paths.append(destination_path.replace('static', ''))  # Adjust path for frontend use

#     return moved_image_paths

    

# # Endpoint to serve the recorded video file
# @app.route('/get_video', methods=['GET'])
# def get_video():
#     file_path = 'video/recorded_video.webm'
#     if os.path.exists(file_path):
#         return send_file(file_path, as_attachment=True)
#     else:
#         return 'File not found'

def formula(ver_h, ver_t, hr_h, hr_t, det_t):
    no_of_units = det_t/(ver_t+hr_t)
    hr_comp = int(str(no_of_units[0]))
    ver_comp = no_of_units-hr_comp
    hr_tr = hr_comp*hr_h
    ver_tr = ver_comp*ver_h
    if hr_tr%2 !=0:
        depth = ver_h-ver_tr
    else:
        depth = ver_tr
    
    return (hr_tr, depth)

# det=[65,78,800,987,1098,3000]
# for i in det:
#     ver_h,ver_t,hr_h,hr_t=91,300,1,5
#     l1=formula(ver_h,ver_t,hr_h,hr_t)


if __name__ == '__main__':
    app.run(debug=True,port='5001')
