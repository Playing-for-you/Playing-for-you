<h1 align='center'>PLAYING FOR YOU: TEXT PROMPT-GUIDED JOINT
AUDIO-VISUAL GENERATION FOR NARRATING FACES
USING MULTI-ENTANGLED LATENT SPACE</h1>

# Goal of the Model compared to SoTA

![Goal](./assets/example.png)

<div align='center'>

Please find the checkpoints for our model that can be loaded into the `torch.load()` function in `train.py` at the following Google-Drive Link:

`https://drive.google.com/drive/folders/12i9uzp_n-eu_5aWiYTsdJAvLM_BUwOIl`
</div>

## Example Generations

<table class="center">

<tr>
    <td style="text-align: center"><b>Source Image</b></td>
    <td style="text-align: center"><b>Prompt Text</b></td>
    <td style="text-align: center"><b>Generated Output</b></td>
    <td style="text-align: center"><b>Description</b></td>
</tr>

<!-- <tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg" width="150">
        </a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px;">
        <b>IN THE DISTRICT COURT LITIGATION ULTIMATELY THERE WERE A NUMBER OF UNANSWERED QUESTIONS AS YOU KNOW A NUMBER OF GAPS THAT WE BELIEVE COULD BE FILLED BY THE GRAND JURY MATERIAL</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/776e66ac-65be-48cf-bc31-13ea6e5c2219" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg" width="150">
            </a>
            <p style="margin: 5px 0 0; font-size: 12px;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px;">
        <b>Sample Generation of a Man</b>
    </td>
</tr> -->

<tr>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg">
            <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg" width="250" height="auto">
        </a>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>IN THE DISTRICT COURT LITIGATION ULTIMATELY THERE WERE A NUMBER OF UNANSWERED QUESTIONS AS YOU KNOW A NUMBER OF GAPS THAT WE BELIEVE COULD BE FILLED BY THE GRAND JURY MATERIAL</b>
    </td>
    <td style="text-align: center; vertical-align: top; min-height: 200px;">
        <div>
            <a href="https://github.com/user-attachments/assets/776e66ac-65be-48cf-bc31-13ea6e5c2219" target="_blank">
                <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg" width="250" height="auto">
            </a>
            <p style="margin: 5px 0 0; font-size: 10px;">Click to play video</p>
        </div>
    </td>
    <td style="text-align: center; vertical-align: middle; min-height: 200px; font-size: 14px;">
        <b>Sample Generation of a Man</b>
    </td>
</tr>


</table>

## News !!

- The model checkpoints can be accessed in the GoogleDrive Link above.
- The following environment must be installed:

Create Conda Environment

```bash
  conda create -n pfy
  conda activate pfy
```
