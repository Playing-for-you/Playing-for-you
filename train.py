import os
import torch
import torch.optim as optim
import torch.nn as nn
import torchaudio
import torchvision
from TTS.config import load_config
from audio_model import CustomXtts as Xtts
from dataset import WildDataset
from tqdm import tqdm
from video_model import get_embeds, Net
from helper import tensor_to_video, resampler, TransformerEncoderSA

from hallo.models.face_locator import FaceLocator
from hallo.models.image_proj import ImageProjModel
from hallo.models.unet_2d_condition import UNet2DConditionModel
from hallo.models.unet_3d import UNet3DConditionModel

from omegaconf import OmegaConf

print("Loading model...")

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# Load TTS configuration and model
tts_config_path = "###########/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json"
tts_checkpoint_dir = "############/tts/tts_models--multilingual--multi-dataset--xtts_v2/"
config = load_config(tts_config_path)
tts_model = Xtts.init_from_config(config)
tts_model.load_checkpoint(config, checkpoint_dir=tts_checkpoint_dir)
tts_model.cuda()

# Set device and weight precision
device = 'cuda'
weight_dtype = torch.float16

# Load inference configuration
config = OmegaConf.load('./hallo/configs/inference/default.yaml')
# Initialize all models needed for the net
reference_unet = UNet2DConditionModel.from_pretrained(config.base_model_path, subfolder="unet")
denoising_unet = UNet3DConditionModel.from_pretrained_2d(
    config.base_model_path,
    config.motion_module_path,
    subfolder="unet",
    unet_additional_kwargs=OmegaConf.to_container(config.unet_additional_kwargs),
    use_landmark=False,
)
face_locator = FaceLocator(conditioning_embedding_channels=320)

image_proj = ImageProjModel(
    cross_attention_dim=denoising_unet.config.cross_attention_dim,
    clip_embeddings_dim=512,
    clip_extra_context_tokens=4,
)

# Combine all models into Net
net = Net(
    reference_unet,
    denoising_unet,
    face_locator,
    image_proj,
)

# Set models to require gradients for training
net.imageproj.requires_grad_(True)
net.reference_unet.requires_grad_(True)
net.denoising_unet.requires_grad_(True)
net.face_locator.requires_grad_(True)

# Enable gradient checkpointing
net.reference_unet.enable_gradient_checkpointing()
net.denoising_unet.enable_gradient_checkpointing()

# Load checkpoint weights for the net
audio_ckpt_dir = config.audio_ckpt_dir
missing_keys, unexpected_keys = net.load_state_dict(
    torch.load(os.path.join(audio_ckpt_dir, "net.pth"), map_location="cpu")
)
assert len(missing_keys) == 0 and len(unexpected_keys) == 0, "Failed to load correct checkpoint."
print(f"Loaded weight from {audio_ckpt_dir}")


# Initialize transformer encoder
audio_transformer_encoder = TransformerEncoderSA(device=device, num_channels=512, num_heads=8).to(device)
video_transformer_encoder = TransformerEncoderSA(device=device, num_channels=512, num_heads=8).to(device)

# Load the training dataset
train_dataset = WildDataset()

# Loss functions
audio_criterion = nn.MSELoss()  # For audio loss
video_criterion = nn.L1Loss()   # For video loss (L1 pixel-wise loss, adjust as needed)

# Define optimizer and scheduler
optimizer = optim.AdamW(list(net.parameters())+ list(video_transformer_encoder.parameters()) + list(audio_transformer_encoder.parameters()) + list(tts_model.parameters()), lr=1e-4, weight_decay=1e-2)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=1000, gamma=0.5)

# # Load model parameters and optimizer state
# checkpoint = torch.load('checkpoints/model/latest.pth')
# tts_model.load_state_dict(checkpoint['tts_model_state_dict'])
# net.load_state_dict(checkpoint['net_state_dict'])
# audio_transformer_encoder.load_state_dict(checkpoint['audio_transformer_encoder_state_dict'])
# video_transformer_encoder.load_state_dict(checkpoint['video_transformer_encoder_state_dict'])
# # Load optimizer state
# optimizer.load_state_dict(torch.load('checkpoints/optim/latest.pth'))
# print("Model and optimizer loaded successfully.")

iter = 0
# Training loop
for epoch in range(25):
    print(f"Started Epoch {epoch + 1}")
    for o, v, t, a, i in tqdm(train_dataset):
        try:
            if os.path.exists(o):
                continue
            print(f"Processing {o}")
            optimizer.zero_grad()  # Reset gradients

            # Read text
            text = open(t, "r").read()
            text = text.strip().lower()
            _, sample_rate = torchaudio.load(a)
            language = "en"  # remove the country code
            text_tokens = torch.IntTensor(tts_model.tokenizer.encode(text, lang=language)).unsqueeze(0).to(device)

            # Get audio conditioning latent and speaker embedding
            gpt_cond_latent, speaker_embedding = tts_model.get_conditioning_latents(
                audio_path=[a], load_sr=sample_rate
            )

            # Get video embeddings and masks
            (
                source_image_lip_region,
                source_image_face_region,
                source_image_face_emb,
                source_image_full_mask,
                source_image_face_mask,
                source_image_lip_mask
            ) = get_embeds(i)
            
            # Reshape embeddings to ensure they have [batch_size, seq_length, 512] format
            reshaped_gpt_cond_latent = gpt_cond_latent.reshape(1, -1, 512).to(device)  # [1, seq_length, 512]
            reshaped_speaker_embedding = speaker_embedding.reshape(1, -1, 512).to(device)  # [1, seq_length, 512]
            padded_text_tokens = torch.zeros(512).to(device)
            padded_text_tokens[:text_tokens.shape[1]] = text_tokens
            reshaped_text_tokens = padded_text_tokens.reshape(1, -1, 512).to(device)  # [1, seq_length, 512]
            
            reshaped_source_image_lip_region = source_image_lip_region.reshape(1, -1, 512).to(device)  # [1, seq_length, 512]
            reshaped_source_image_face_region = source_image_face_region.reshape(1, -1, 512).to(device)  # [1, seq_length, 512]
            reshaped_source_image_face_emb = torch.tensor(source_image_face_emb).reshape(1, 1, 512).to(device)  # [1, 1, 512]
            
            seq_len_text_tokens = reshaped_text_tokens.shape[1]
            seq_len_gpt_cond_latent = reshaped_gpt_cond_latent.shape[1]
            seq_len_speaker_embedding = reshaped_speaker_embedding.shape[1]

            concatenated_video_emb = torch.cat([
                reshaped_source_image_lip_region,
                reshaped_source_image_face_region,
                reshaped_source_image_face_emb,
                reshaped_text_tokens,
            ], dim=1).to(torch.float32)    
            
            
            
            concatenated_audio_emb = torch.cat([
                reshaped_gpt_cond_latent,
                reshaped_speaker_embedding,
            ], dim=1).to(torch.float32)        

            audio_comb_emb = audio_transformer_encoder(concatenated_audio_emb, concatenated_video_emb)

            # Output Processing (Extract individual embeddings from transformer output)
            # Extract embeddings back from the transformer output
            extracted_gpt_cond_latent = audio_comb_emb[:, seq_len_text_tokens :seq_len_text_tokens + seq_len_gpt_cond_latent, :].reshape(1, 32, 1024)
            extracted_speaker_embedding = audio_comb_emb[:, seq_len_text_tokens + seq_len_gpt_cond_latent:, :].reshape(1, 512, 1)

            # Generate audio output
            audio_out = tts_model.pipeline(
                text_tokens,
                extracted_gpt_cond_latent,
                extracted_speaker_embedding,
            )

            
            concatenated_video_emb = torch.cat([
                reshaped_source_image_lip_region,
                reshaped_source_image_face_region,
                reshaped_source_image_face_emb,
            ], dim=1).to(torch.float32)    
            
            
            concatenated_audio_emb = torch.cat([
                reshaped_text_tokens,
                reshaped_gpt_cond_latent,
                reshaped_speaker_embedding,
            ], dim=1).to(torch.float32)     
            
            video_comb_emb = video_transformer_encoder(concatenated_video_emb, concatenated_audio_emb)
            
            seq_source_image_lip_region = reshaped_source_image_lip_region.shape[1]
            seq_source_image_face_region = reshaped_source_image_face_region.shape[1]
            seq_source_image_face_emb = reshaped_source_image_face_emb.shape[1]
            
            # Extract embeddings back from the transformer output
            extracted_source_image_lip_region = video_comb_emb[:, :seq_source_image_lip_region, :].reshape(3, 512, 512)
            extracted_source_image_face_region = video_comb_emb[:, seq_source_image_lip_region:seq_source_image_lip_region + seq_source_image_face_region, :].reshape(3, 512, 512)
            extracted_source_image_face_emb = video_comb_emb[:, seq_source_image_lip_region + seq_source_image_face_region:, :].reshape(512)
            
            # Generate video output
            tensor_result = net.pipeline(
                extracted_source_image_lip_region,
                extracted_source_image_face_region,
                extracted_source_image_face_emb,
                source_image_full_mask,
                source_image_face_mask,
                source_image_lip_mask,
            )

            # Prepare ground truth audio
            ground_truth_audio, sample_rate = torchaudio.load(v)
            resampled_audio = resampled_audio.unsqueeze(0)
            ground_truth_audio = resampler(ground_truth_audio, sample_rate).cuda()
            resampled_audio = resampler(audio_out['wav']).cuda()
            alen = min(resampled_audio.shape[1], ground_truth_audio.shape[1])
            # Audio loss (e.g., MSE loss between generated audio and ground truth)
            audio_loss = audio_criterion(resampled_audio[:, :alen], ground_truth_audio[:, :alen])

            # Video loss (L1 pixel-wise loss between predicted and original frames)
            # read video from v
            ground_truth_video = torchvision.io.read_video(v)[0].permute(3, 0, 1, 2).cuda() / 255.0
            resize = torchvision.transforms.Resize((512, 512))
            tensor_resized = torch.stack([resize(t) for t in ground_truth_video.permute(1, 0, 2, 3)])
            tensor_resized = tensor_resized.permute(1, 0, 2, 3)
            vlen = min(tensor_result.shape[1], tensor_resized.shape[1])
            tensor_result = tensor_result.cuda()
            video_loss = video_criterion(tensor_result[:, :vlen], tensor_resized[:, :vlen])

            # Joint loss: combine audio and video losses
            joint_loss = config.hy*audio_loss + video_loss

            # Backpropagate joint loss
            joint_loss.backward()

            # Update model parameters
            optimizer.step()

            # Optional: Step the scheduler
            scheduler.step()

            # Save outputs
            tensor_to_video(tensor_result.detach().cpu(), o.replace('__',f'_{iter:04}_'), resampled_audio.detach().cpu())
            # Print loss for monitoring
            print(f"Iter {iter}: Audio Loss: {audio_loss.item()}, Video Loss: {video_loss.item()}, Joint Loss: {joint_loss.item()}")
            
            if iter%100 == 0:
                model_save_path = f'checkpoints/model/{iter}.pth'
                optimizer_save_path = f'checkpoints/optim/{iter}.pth'
                torch.save({
                    # 'tts_model_state_dict': tts_model.state_dict(),
                    'net_state_dict': net.state_dict(),
                    'audio_transformer_encoder_state_dict': audio_transformer_encoder.state_dict(),
                    'video_transformer_encoder_state_dict': video_transformer_encoder.state_dict(),
                }, model_save_path)

                # Save optimizer state
                torch.save(optimizer.state_dict(), optimizer_save_path)

                model_save_path = f'checkpoints/model/latest.pth'
                optimizer_save_path = f'checkpoints/optim/latest.pth'
                torch.save({
                    # 'tts_model_state_dict': tts_model.state_dict(),
                    'net_state_dict': net.state_dict(),
                    'audio_transformer_encoder_state_dict': audio_transformer_encoder.state_dict(),
                    'video_transformer_encoder_state_dict': video_transformer_encoder.state_dict(),
                }, model_save_path)

                # Save optimizer state
                torch.save(optimizer.state_dict(), optimizer_save_path)
                print("Model and optimizer saved successfully.")
            iter += 1
        
        except Exception as e:
            print(f"Error occurred: {e} during processing {o}")
            continue
print("Training complete!")
