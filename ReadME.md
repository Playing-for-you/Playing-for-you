<h1 align='center'>PLAYING FOR YOU: TEXT PROMPT-GUIDED JOINT
AUDIO-VISUAL GENERATION FOR NARRATING FACES
USING MULTI-ENTANGLED LATENT SPACE</h1>

# Goal of the Model compared to SoTA

![Goal](./assets/example.png)

<div align='center'>

Please find the checkpoints for our model that can be loaded into the `torch.load()` function in `train.py` at the following Google-Drive Link:

<a href="https://drive.google.com/drive/folders/12i9uzp_n-eu_5aWiYTsdJAvLM_BUwOIl">Checkpoints</a>

</div>

## Example Generations

<table class="center">

<tr>
    <td style="text-align: center"><b>Source Image</b></td>
    <td style="text-align: center"><b>Audio Profile</b></td>
    <td style="text-align: center"><b>Prompt Text</b></td>
    <td style="text-align: center"><b>Generated Output</b></td>
    <td style="text-align: center"><b>Description</b></td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/1rv2A4vXVJLxcEgyc8JIgP_P1fLS-oP3c/view?usp=drive_link">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>IN THE DISTRICT COURT LITIGATION ULTIMATELY THERE WERE A NUMBER OF UNANSWERED QUESTIONS AS YOU KNOW A NUMBER OF GAPS THAT WE BELIEVE COULD BE FILLED BY THE GRAND JURY MATERIAL</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/776e66ac-65be-48cf-bc31-13ea6e5c2219" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Sample Generation of a Man</b>
    </td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/oldMan.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/oldMan.jpg" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/19LXUnLc_0YkULgNH_pyi54jxT-lAXdEh/view?usp=drive_link">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>OR PRODUCERS OR PROCESSORS OR ACCOUNTANTS OR AGRONOMISTS THE LIGHT BULB GOES ON I'VE SEEN IT OVER AND OVER AND PEOPLE WILL SAY WELL WE'RE DOING THIS</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/7f803bfd-0733-428b-9a04-03e619c4ca29" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/oldMan.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Sample Generation of an older man</b>
    </td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/oldMan2.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/oldMan2.jpg" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/13VHgGYYwfjf1s8FwuU_YJ5TQtA4xmxF5/view?usp=drive_link">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>GRANTED THAT I'VE BEEN AROUND FOR A WHILE AND DECIDED THEY'LL GET ME IN NOVEMBER SO TO SPEAK BUT I DON'T THINK WE CAN REALLY GO BACK AND RELITIGATE THAT ASPECT OF IT</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/e4bc7bb0-ce73-4690-a511-3655cf5f1a72" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/oldMan2.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Sample Generation of another old man</b>
    </td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/Woman.png">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/Woman.png" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/12cbSWPZ95NFnFcGE2OLHq5kHMa9tVtvk/view?usp=sharing">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>EVERYBODY THIS IS SENATOR MARSHA BLACKBURN FROM THE STATE OF TENNESSE AND I'M JUST SO EXCITED TO BE A PART OF THIS CELEBRATION</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/9c296f77-376d-42fb-8891-1809c4005a3c" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/Woman.png" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Sample Generation of a woman</b>
    </td>

</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/Woman.png">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/Woman.png" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/1yhs1mbK6gIJpQ6NDn8InkmQrxhj9rS4A/view?usp=sharing">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>EVERYBODY THIS IS SENATOR MARSHA BLACKBURN FROM THE STATE OF TENNESSE AND I'M JUST SO EXCITED TO BE A PART OF THIS CELEBRATION</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/35e5a622-a14b-47b0-9056-f4a0d556a105" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/Woman.png" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Generation of the same woman but with a degraded audio input, generated using a reduced bitrate, downsampling the audio, and adding distortion.</b>
    </td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/kid_1.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/kid_1.jpg" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/1nSdjIZs4DXQnGe-GMBkOnnpqSR-07VCO/view?usp=drive_link">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>SOMETIMES, THE BEST THING YOU CAN DO IS TO LET GO</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/7142cbd5-d150-4017-9648-6494ac04868f" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/kid_1.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Random child image from the internet, with an adult female voice profile as input.</b>
    </td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/kid_2.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/kid_2.jpg" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/1GSZqPv2uANQciv6IDQ03zZ8TWTL_SAyE/view?usp=sharing">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>BE THE CHANGE YOU WANT TO SEE IN THE WORLD, BROTHERS AND SISTERS.</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/30d003a2-f3d3-4009-be9e-3ed3db680c71" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/kid_2.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>A Stable-Diffusion Generated Image of a child from the internet, with an adult male voice as input.</b>
    </td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/actor.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/actor.jpg" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/1U-XXmuJhmq_RGeZ6vVeEbetXFQze8yv8/view?usp=sharing">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>I INVISCATE THE PAPER WITH GLUE TO CREATE MY ART PROJECT.</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/b87b84d4-18fa-43cf-b2a2-294aef90eecd" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/actor.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Voice profile of a child, with the face of an adult man.</b>
    </td>
</tr>

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/indian2.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/indian2.jpg" width="250" height="auto">
        </a>
    </td>
    <td>
        <a href="https://drive.google.com/file/d/1mJvm3rRuXH24LP9wWXxEZJGXi7sDKbeG/view?usp=drive_link">Audio</a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>PEOPLE DO WHAT THEY HATE FOR MONEY, AND USE THE MONEY TO DO WHAT THEY LOVE.</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/a6065341-dfc4-47e5-ab0c-6cf314331988" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/indian2.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px; text-align: center;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Generation of an Indian Man.</b>
    </td>
</tr>

</table>

## News !!

- The model checkpoints can be accessed in the GoogleDrive Link above.
- Data Samples can be found at the following link: <a href="https://drive.google.com/file/d/1dmdv6k8XaWzhe22szvjPw6XxXL3sIkcp/view?usp=sharing">Data</a>
- The following packages must be installed into your environment:

```bash
  pip install -r requirements.txt
```

- We will soon be publishing our model on Hugging Face 🤗

## Files:

- `preprocess.py` processes the multimodal inputs required for our model
- The `helper.py` file has our transformer architectures and other helper functions
- `get_videos.py` makes the train-test split and saves the outputs to the desired folder, clipping it to the desired length
- The `audio_model.py` and `video_model.py` files have the definitions of our models, which are called in the train.py file
- The assets folder has some example outputs, that can be viewed in the ReadME.md file of this repository
