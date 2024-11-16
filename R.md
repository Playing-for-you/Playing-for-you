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

<tr>
    <td style="text-align: center"><a target="_blank" href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg"><img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg"></a></td>
    <td style="text-align: center"><b>OR PRODUCERS OR PROCESSORS OR ACCOUNTANTS OR AGRONOMISTS THE LIGHT BULB GOES ON I'VE SEEN IT OVER AND OVER AND PEOPLE WILL SAY WELL WE'RE DOING THIS</b></td>
    <td style="text-align: center">
      <a href="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Videos/man.mp4?raw=true" target="_blank">
        <img src="https://github.com/Playing-for-you/Playing-for-you/blob/main/assets/Images/man.jpg" alt="Man Thumbnail" width="250">
      </a>
      <p>Click to play video</p>
    </td>
    <td style="text-align: center"><b>A sample generation of a man speaking</b></td>
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