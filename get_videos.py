import os
import glob
import random

# path = '##############/vox'
# path = '###############/FakeAVCeleb_v1.2/RealVideo-RealAudio'
# path = '##########/celebv-hq/35666'
# path = '#############/HDTF-dataset/HDTF-RGB-512'
files = [f for f in glob.glob(os.path.join(path, '*.mp4')) if os.path.isfile(f)]
random.shuffle(files)

copy_path = '/####################/train/videos/'
print(len(files))
train = 0.8 * len(files)
for idx, file in enumerate(files[:train]):
    if not os.path.exists(copy_path):
        os.makedirs(copy_path)
    dest_path = os.path.join(copy_path, f'0{idx:03}.mp4')
    os.system(f'ffmpeg -ss 0 -t 10 -i "{file}" -c copy "{dest_path}" -loglevel quiet')
    print(file, dest_path)