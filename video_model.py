import torch
import torch.nn as nn
from diffusers import AutoencoderKL, DDIMScheduler
from omegaconf import OmegaConf

from hallo.animate.face_animate import FaceAnimatePipeline
from hallo.datasets.image_processor import ImageProcessor
from hallo.models.face_locator import FaceLocator
from hallo.models.unet_2d_condition import UNet2DConditionModel
from hallo.models.unet_3d import UNet3DConditionModel

class Net(nn.Module):
    def __init__(
        self,
        reference_unet: UNet2DConditionModel,
        denoising_unet: UNet3DConditionModel,
        face_locator: FaceLocator,
        imageproj,
    ):
        super().__init__()
        self.reference_unet = reference_unet
        self.denoising_unet = denoising_unet
        self.face_locator = face_locator
        self.imageproj = imageproj

    def forward(self,):
        pass
    def get_modules(self):
        return {
            "reference_unet": self.reference_unet,
            "denoising_unet": self.denoising_unet,
            "face_locator": self.face_locator,
            "imageproj": self.imageproj,
            "audioproj": self.audioproj,
        }

    
    def pipeline(self,
        source_image_pixels, 
        source_image_face_region, 
        source_image_face_emb, 
        source_image_full_mask, 
        source_image_face_mask, 
        source_image_lip_mask, 
        config_path: str = 'hallo/configs/inference/default.yaml',
    ):
        config = OmegaConf.load(config_path)
        motion_scale = [config.pose_weight, config.face_weight, config.lip_weight]
        
        device = torch.device(
            "cuda") if torch.cuda.is_available() else torch.device("cpu")
        if config.weight_dtype == "fp16":
            weight_dtype = torch.float16

        sched_kwargs = OmegaConf.to_container(config.noise_scheduler_kwargs)
        if config.enable_zero_snr:
            sched_kwargs.update(
                rescale_betas_zero_snr=True,
                timestep_spacing="trailing",
                prediction_type="v_prediction",
            )
        val_noise_scheduler = DDIMScheduler(**sched_kwargs)
        sched_kwargs.update({"beta_schedule": "scaled_linear"})

        vae = AutoencoderKL.from_pretrained(config.vae.model_path)
        

        vae.requires_grad_(True)


        pipeline = FaceAnimatePipeline(
            vae=vae,
            reference_unet=self.reference_unet,
            denoising_unet=self.denoising_unet,
            face_locator=self.face_locator,
            scheduler=val_noise_scheduler,
            image_proj=self.imageproj,
        )
        pipeline.to(device=device, dtype=weight_dtype)

        source_image_pixels = source_image_pixels.unsqueeze(0)
        source_image_face_region = source_image_face_region.unsqueeze(0)
        source_image_face_emb = source_image_face_emb.reshape(1, -1)
        source_image_face_emb = torch.tensor(source_image_face_emb)
        
        img_size = (config.data.source_image.width,
                    config.data.source_image.height)
        clip_length = config.data.n_sample_frames
        source_image_full_mask = [
            (mask.repeat(clip_length, 1))
            for mask in source_image_full_mask
        ]
        source_image_face_mask = [
            (mask.repeat(clip_length, 1))
            for mask in source_image_face_mask
        ]
        source_image_lip_mask = [
            (mask.repeat(clip_length, 1))
            for mask in source_image_lip_mask
        ]

        tensor_result = []

        generator = torch.manual_seed(42)

        if len(tensor_result) == 0:
            # The first iteration
            motion_zeros = source_image_pixels.repeat(
                config.data.n_motion_frames, 1, 1, 1)
            motion_zeros = motion_zeros.to(
                dtype=source_image_pixels.dtype, device=source_image_pixels.device)
            pixel_values_ref_img = torch.cat(
                [source_image_pixels, motion_zeros], dim=0)  # concat the ref image and the first motion frames
        else:
            motion_frames = tensor_result[-1][0]
            motion_frames = motion_frames.permute(1, 0, 2, 3)
            motion_frames = motion_frames[0-config.data.n_motion_frames:]
            motion_frames = motion_frames * 2.0 - 1.0
            motion_frames = motion_frames.to(
                dtype=source_image_pixels.dtype, device=source_image_pixels.device)
            pixel_values_ref_img = torch.cat(
                [source_image_pixels, motion_frames], dim=0)  # concat the ref image and the motion frames

        pixel_values_ref_img = pixel_values_ref_img.unsqueeze(0)

        pipeline_output = pipeline(
            ref_image=pixel_values_ref_img,
            face_emb=source_image_face_emb,
            face_mask=source_image_face_region,
            pixel_values_full_mask=source_image_full_mask,
            pixel_values_face_mask=source_image_face_mask,
            pixel_values_lip_mask=source_image_lip_mask,
            width=img_size[0],
            height=img_size[1],
            video_length=clip_length,
            num_inference_steps=config.inference_steps,
            guidance_scale=config.cfg_scale,
            generator=generator,
            motion_scale=motion_scale,
        )

        tensor_result = pipeline_output.videos
        tensor_result = tensor_result.squeeze(0)

        return tensor_result

def get_embeds(
    source_image_path: str,
    config_path: str = './hallo/configs/inference/default.yaml',
):
    # 1. init config    
    config = OmegaConf.load(config_path)
    source_image_path = source_image_path
    save_path = './hallo/.cache'
    
    # 3. prepare inference data
    # 3.1 prepare source image, face mask, face embeddings
    img_size = (config.data.source_image.width,
                config.data.source_image.height)
    face_analysis_model_path = config.face_analysis.model_path
    with ImageProcessor(img_size, face_analysis_model_path) as image_processor:
        source_image_pixels, \
        source_image_face_region, \
        source_image_face_emb, \
        source_image_full_mask, \
        source_image_face_mask, \
        source_image_lip_mask = image_processor.preprocess(
            source_image_path, save_path, config.face_expand_ratio)

    return source_image_pixels, source_image_face_region, source_image_face_emb, source_image_full_mask, source_image_face_mask, source_image_lip_mask

