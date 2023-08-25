# AnimateDiff Local Fine Tuning
This repo is only for fine tuning motion modules, locally. It is based on the work of Tumurzakov, and with much help from Cubey and many others.

Results "may" vary, use at your own discretion, offer void where prohibited. No gaurantees or promises.

# HEAVILY WIP

Usage:

*linux see end*

-git clone https://github.com/B34STW4RS/AD-Evo-Tuner/

 -cd AD-Evo-Tuner

-conda env create -f environment.yaml

-conda activate adt

-place motion modules in models/motion_module/

-place runwayml sd1.5 files in models/stablediffusion/

-unpacked don't need safetensors etc.

-make a dataset similar to the default example set, including a populated caption.txt and validate.txt*

*validate currently mostly non-functional wip*
*sample dataset is a baseline of what you could probably train*
*report issues with terminal outputs*
*there are some nags you can ignore don't worry about them for now*

- run adt-user.bat
- name your project
- select the motion module you wish to fine tune
- select your dataset folder
- hit start
- ????
- profit
*models will be output to models/motion_module/{project_name+time}*
*config will be saved to configs/training/{project_name+time.yaml}*

# To Do:
 - rewrite gui
 - implement more viable parameters
 - fix validation
 - improve documentation
 - post sample models to civit.ai
 - post sample gifs from finetuned motion modules
 - data preprocessor
 - purple monkey dishwasher

# On Linux // Temporary solution
After solving the environment and activating it
- pip uninstall xformers
- pip install xformers==0.0.20
- pip install triton==2.0.0

#Advanced
Advanced users can forgo using the gui entirely, and directly copy the default.yaml in the training directory and modify it as they wish.
- run python train.py --config pathto/config.yaml

# AnimateDiff

<a target="_blank" href="https://colab.research.google.com/github/tumurzakov/AnimateDiff/blob/main/Fine_tune_AnimateDiff.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

This repository is the official implementation of [AnimateDiff](https://arxiv.org/abs/2307.04725).

**[AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning](https://arxiv.org/abs/2307.04725)**
</br>
Yuwei Guo,
Ceyuan Yang*,
Anyi Rao,
Yaohui Wang,
Yu Qiao,
Dahua Lin,
Bo Dai

<p style="font-size: 0.8em; margin-top: -1em">*Corresponding Author</p>

[Arxiv Report](https://arxiv.org/abs/2307.04725) | [Project Page](https://animatediff.github.io/)


```
### Download Base T2I & Motion Module Checkpoints
We provide two versions of our Motion Module, which are trained on stable-diffusion-v1-4 and finetuned on v1-5 seperately.
It's recommanded to try both of them for best results.
```
git lfs install
git clone https://huggingface.co/runwayml/stable-diffusion-v1-5 models/StableDiffusion/

bash download_bashscripts/0-MotionModule.sh
```
You may also directly download the motion module checkpoints from [Google Drive](https://drive.google.com/drive/folders/1EqLC65eR1-W-sGD0Im7fkED6c8GkiNFI?usp=sharing), then put them in `models/Motion_Module/` folder.

### Prepare Personalize T2I
Here we provide inference configs for 6 demo T2I on CivitAI.
You may run the following bash scripts to download these checkpoints.
```
bash download_bashscripts/1-ToonYou.sh
bash download_bashscripts/2-Lyriel.sh
bash download_bashscripts/3-RcnzCartoon.sh
bash download_bashscripts/4-MajicMix.sh
bash download_bashscripts/5-RealisticVision.sh
bash download_bashscripts/6-Tusun.sh
bash download_bashscripts/7-FilmVelvia.sh
bash download_bashscripts/8-GhibliBackground.sh
```

### Inference
After downloading the above peronalized T2I checkpoints, run the following commands to generate animations. The results will automatically be saved to `samples/` folder.
```
python -m scripts.animate --config configs/prompts/1-ToonYou.yaml
python -m scripts.animate --config configs/prompts/2-Lyriel.yaml
python -m scripts.animate --config configs/prompts/3-RcnzCartoon.yaml
python -m scripts.animate --config configs/prompts/4-MajicMix.yaml
python -m scripts.animate --config configs/prompts/5-RealisticVision.yaml
python -m scripts.animate --config configs/prompts/6-Tusun.yaml
python -m scripts.animate --config configs/prompts/7-FilmVelvia.yaml
python -m scripts.animate --config configs/prompts/8-GhibliBackground.yaml
```

To generate animations with a new DreamBooth/LoRA model, you may create a new config `.yaml` file in the following format:
```
NewModel:
  path: "[path to your DreamBooth/LoRA model .safetensors file]"
  base: "[path to LoRA base model .safetensors file, leave it empty string if not needed]"

  motion_module:
    - "models/Motion_Module/mm_sd_v14.ckpt"
    - "models/Motion_Module/mm_sd_v15.ckpt"
    
  steps:          25
  guidance_scale: 7.5

  prompt:
    - "[positive prompt]"

  n_prompt:
    - "[negative prompt]"
```
Then run the following commands:
```
python -m scripts.animate --config [path to the config file]
```


## BibTeX
```
@misc{guo2023animatediff,
      title={AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning}, 
      author={Yuwei Guo, Ceyuan Yang, Anyi Rao, Yaohui Wang, Yu Qiao, Dahua Lin, Bo Dai},
      year={2023},
      eprint={2307.04725},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## Contact Us
**Yuwei Guo**: [guoyuwei@pjlab.org.cn](mailto:guoyuwei@pjlab.org.cn)  
**Ceyuan Yang**: [yangceyuan@pjlab.org.cn](mailto:yangceyuan@pjlab.org.cn)  
**Bo Dai**: [daibo@pjlab.org.cn](mailto:daibo@pjlab.org.cn)

## Acknowledgements
Codebase built upon [Tune-a-Video](https://github.com/showlab/Tune-A-Video).
