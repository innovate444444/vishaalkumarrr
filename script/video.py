import cv2
import os

def extract_frames(video_path, output_folder, frame_interval=60):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_count = 0

    # Loop through the video and extract frames at the specified interval
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Extract frames at the specified interval
        if frame_count % frame_interval == 0:
            # Save frame as PNG with frame number in the filename
            frame_name = f"frame_{frame_count:08d}.png"
            frame_path = os.path.join(output_folder, frame_name)
            cv2.imwrite(frame_path, frame)
            extracted_count += 1

        frame_count += 1

    cap.release()
    print(f"{extracted_count} frames extracted successfully.")

# # Provide the path to your .webm video file and output folder
# video_file_path = 'video/recorded_video.webm'
# output_folder_path = 'frames'

# extract_frames(video_file_path, output_folder_path, frame_interval=60)
