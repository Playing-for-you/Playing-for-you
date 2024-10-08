from TTS.tts.models.xtts import Xtts
import torch
import torch.nn.functional as F

class CustomXtts(Xtts):
    def pipeline(
        self,
        text_tokens,
        gpt_cond_latent,
        speaker_embedding,
        # GPT inference
        temperature=0.75,
        length_penalty=1.0,
        repetition_penalty=10.0,
        top_k=50,
        top_p=0.85,
        do_sample=True,
        num_beams=1,
        speed=1.0,
        **hf_generate_kwargs,
    ):
        
        length_scale = 1.0 / max(speed, 0.05)
        gpt_cond_latent = gpt_cond_latent.to(self.device)
        speaker_embedding = speaker_embedding.to(self.device)

        wavs = []
        gpt_latents_list = []

        gpt_codes = self.gpt.generate(
            cond_latents=gpt_cond_latent,
            text_inputs=text_tokens,
            input_tokens=None,
            do_sample=do_sample,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            num_return_sequences=self.gpt_batch_size,
            num_beams=num_beams,
            length_penalty=length_penalty,
            repetition_penalty=repetition_penalty,
            output_attentions=False,
            **hf_generate_kwargs,
        )
        expected_output_len = torch.tensor(
            [gpt_codes.shape[-1] * self.gpt.code_stride_len], device=text_tokens.device
        )

        text_len = torch.tensor([text_tokens.shape[-1]], device=self.device)
        gpt_latents = self.gpt(
            text_tokens,
            text_len,
            gpt_codes,
            expected_output_len,
            cond_latents=gpt_cond_latent,
            return_attentions=False,
            return_latent=True,
        )

        if length_scale != 1.0:
            gpt_latents = F.interpolate(
                gpt_latents.transpose(1, 2), scale_factor=length_scale, mode="linear"
            ).transpose(1, 2)

        gpt_latents_list.append(gpt_latents.cpu())
        wavs.append(self.hifigan_decoder(gpt_latents, g=speaker_embedding).cpu().squeeze())

        return {
            "wav": torch.cat(wavs, dim=0),
            "gpt_latents": torch.cat(gpt_latents_list, dim=1),
            "speaker_embedding": speaker_embedding,
        }
