import os
import glob
from torch.utils.data import Dataset
import random

class WildDataset(Dataset):
    def __init__(self, data_dir=''):
        self.data_dir = data_dir
        self.files = glob.glob(os.path.join(self.data_dir, 'texts', '*.txt'))
        self.files = sorted(self.files)
        random.seed(42)
        random.shuffle(self.files)
        
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        text_path = self.files[idx]
        video_path = text_path.replace('texts', 'videos').replace('.txt', '.mp4')
        image_path = video_path.replace('videos', 'images').replace('.mp4', '.jpg')
        audio_path = video_path.replace('videos', 'ref_audios').replace('.mp4', '.wav')
        output_path = video_path.replace('videos/', 'outputs/iter__')
        return output_path, video_path, text_path, audio_path, image_path

                
if __name__ == '__main__':
    test_dataset = WildDataset()