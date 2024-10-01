import os
import re
import moviepy.editor as mp
import whisper
from tqdm import tqdm

path = '#################/train/videos'
files = os.listdir(path)
video_files = [file for file in files if file.endswith('.mp4')]
video_files = sorted(video_files)
l = len(video_files)
model = whisper.load_model("medium.en", device="cuda")

def preprocess_images(video_file):
    # Extract the image frames from the video
    image_path = video_file.replace('videos','images').replace('.mp4', '.jpg')
    video = mp.VideoFileClip(video_file)
    video.save_frame(image_path, t=0)
            
def preprocess_texts(video_file):
    text_path = video_file.replace('videos', 'texts').replace('.mp4', '.txt')

    result = model.transcribe(video_file)
    transcript = (
        re.sub(r"[\,\?\.\!\-\;\:\"]", "", result["text"])
        .upper()
        .replace("’", "'")
    )
    transcript = " ".join(transcript.split())
    
    with open(text_path, 'w') as file:
        file.write(transcript)

def preprocess(file):
    try:
        # print("Processing file:", file)
        file = os.path.join(path, file)  # Use os.path.join to concatenate the directory and file name
        # Preprocess images
        preprocess_images(file)
        # Preprocess texts
        preprocess_texts(file)
    except Exception as e:
        print("Error processing file:", file, e)
        txt_file = file.replace('videos', 'texts').replace('.mp4', '.txt')
        image_file = file.replace('videos', 'images').replace('.mp4', '.jpg')

        if os.path.exists(txt_file):
            os.remove(txt_file)
        if os.path.exists(file):
            os.remove(file)
        if os.path.exists(image_file):
            os.remove(image_file)

print("Started")
for file in tqdm(video_files):
    preprocess(file)
print("Finished")