import numpy as np

import torchaudio
from moviepy.editor import AudioFileClip, VideoClip
import tempfile

def resampler(audio, orig_freq=24000, new_freq=16000):
    """
    Resample the audio to the new frequency.

    Parameters:
        audio (torch.Tensor): The audio tensor to resample.
        orig_freq (int, optional): The original frequency of the audio.
        new_freq (int, optional): The new frequency to resample the audio to.

    Returns:
        resampled_audio (torch.Tensor): The resampled audio tensor.
    """
    resampler = torchaudio.transforms.Resample(orig_freq=orig_freq, new_freq=new_freq)
    resampled_audio = resampler(audio)
    resampled_audio = resampled_audio
    return resampled_audio


def tensor_to_video(tensor, output_video_file, audio_source, fps=25):
    """
    Converts a Tensor with shape [c, f, h, w] into a video and adds an audio track from the specified audio file.

    Args:
        tensor (Tensor): The Tensor to be converted, shaped [c, f, h, w].
        output_video_file (str): The file path where the output video will be saved.
        audio_source (str): The path to the audio file (WAV file) that contains the audio track to be added.
        fps (int): The frame rate of the output video. Default is 25 fps.
    """
    tensor = tensor.permute(1, 2, 3, 0).cpu(
    ).numpy()  # convert to [f, h, w, c]
    tensor = np.clip(tensor * 255, 0, 255).astype(
        np.uint8
    )  # to [0, 255]

    def make_frame(t):
        # get index
        frame_index = min(int(t * fps), tensor.shape[0] - 1)
        return tensor[frame_index]
    
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
        torchaudio.save(temp_audio_file.name, audio_source, 16000)
        new_video_clip = VideoClip(make_frame, duration=tensor.shape[0] / fps)
        audio_clip = AudioFileClip(temp_audio_file.name).subclip(0, tensor.shape[0] / fps)
        new_video_clip = new_video_clip.set_audio(audio_clip)
        new_video_clip.write_videofile(output_video_file, fps=fps, audio_codec='aac')

import torch
import torch.nn as nn

class TransformerEncoderSA(nn.Module):
    def __init__(self, device, num_channels: int = 512, num_heads: int = 1):
        """
        A transformer encoder block that takes two embeddings of different sizes and applies attention.
        """
        super(TransformerEncoderSA, self).__init__()
        self.device = device
        self.num_channels = num_channels

        # Multi-head attention with the specified number of heads
        self.mha = nn.MultiheadAttention(
            embed_dim=num_channels, num_heads=num_heads, batch_first=True, bias=False
        ).to(self.device)  # Move to the correct device
        self.mha.in_proj_weight.data.fill_(0.0)  # Set input projections to zero
        self.mha.out_proj.weight.data.fill_(0.0)  # Set output projection to zero

        # Layer Normalization
        self.ln = nn.LayerNorm([num_channels], elementwise_affine=True).to(self.device)
        self.ln.weight.data.fill_(1.0)

        # Feed-forward network
        self.ff_self = nn.Sequential(
            nn.LayerNorm([num_channels], elementwise_affine=True).to(self.device),
            nn.Linear(in_features=num_channels, out_features=num_channels, bias=False).to(self.device),
            nn.LayerNorm([num_channels], elementwise_affine=True).to(self.device),
            nn.Linear(in_features=num_channels, out_features=num_channels, bias=False).to(self.device),
        )
        self.ff_self[0].weight.data.fill_(0.0)
        self.ff_self[2].weight.data.fill_(0.0)
        self.ff_self[1].weight.data.fill_(0.0)
        self.ff_self[3].weight.data.fill_(0.0)

    def forward(self, x: torch.Tensor, y :torch.Tensor) -> torch.Tensor:
        """
        Forward pass for attention between two embeddings.

        """
        x_ln = self.ln(x)
        y_ln = self.ln(y)
        attention_value, _ = self.mha(query=x_ln, key=y_ln, value=y_ln)
        attention_value = attention_value + x
        attention_value = self.ff_self(attention_value) + attention_value
        return attention_value