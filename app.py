


from flask import Flask, request, jsonify,render_template, request, jsonify,redirect,session
import os
import uuid
import cv2
import shutil
import os
import sqlite3

import backend
import json

app = Flask(__name__)



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
        rust_result = backend.corrosionx(threshold_values)
        print(rust_result)

    return render_template('rust.html', rust=rust_result)




@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        file_path = 'video/recorded_video.webm'  

        # Delete the existing file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Save the new uploaded file
        file.save(file_path)

        import backend    
        backend.frame_extraction()

        backend.enhancement()
        
       
        detected_cracks=backend.crack_processing()
        det_t = [int(path[-7:-4]) for path in detected_cracks]
        det_t_divided = [value / 30 for value in det_t]
        data_to_send = [backend.formula(20, 180, 1, 5, i) for i in det_t_divided]

        @app.route('/send_data')
        def send_data():
            return jsonify(data=data_to_send)

        rust=backend.corrosionx(threshold_values)
        print(rust)

        output_folder = 'static/images/crack'

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        else:
            existing_files = os.listdir(output_folder)
            for file in existing_files:
                file_path = os.path.join(output_folder, file)
                os.remove(file_path)

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
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        else:
            existing_files = os.listdir(output_folder)
            for file in existing_files:
                file_path = os.path.join(output_folder, file)
                os.remove(file_path)

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




@app.route('/threshold')
def threshold():
    return render_template('threshold_form.html')
threshold_values = {
    "no_corrosion": 0,
    "very_low": 10000,
    "low": 100000,
    "medium": 300000,
    "high": 500000,
    "very_high": 800000
}

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    user_values = {key: int(request.form[key]) for key in threshold_values.keys()}
    
    # Validate user input
    for key, value in user_values.items():
        if value < 0:
            return f"Invalid value for {key}: Value must be >= 0"
    
    # Update threshold values
    threshold_values.update(user_values)
    print(threshold_values)
    
    # Redirect to the form page or perform any other action
    return render_template('threshold_form.html', success=True)

x,y,z=2324345,6789765476,2929857
def emer(x,y,z):
    opt_high_x=190909
    opt_low_x=-86655
    opt_high_y=32456988
    opt_low_y=-190909
    opt_high_z=4342436
    opt_low_z=-97856
    if (x<opt_low_x or x>opt_high_x):
        emer()
    elif(y<opt_low_y or y>opt_high_y):
        emer()
    elif(z<opt_low_z or z>opt_high_z):
        emer()
   
    



if __name__ == '__main__':
    app.run(debug=True,port='5001')
