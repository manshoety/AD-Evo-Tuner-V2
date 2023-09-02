#!/bin/bash

# activate the conda environment
conda activate adt

# Download runwayml/StableDiffusion
echo "Downloading runwayml/StableDiffusion..."
python EZ_Facehugger.py

# Download the motion modules
echo "Downloading motion modules..."

if [ ! -f "models/Motion_Module/mm_sd_v14.ckpt" ]; then
    gdown "1RqkQuGPaCO5sGZ6V6KZ-jUWmsRu48Kdq" -O "models/Motion_Module/mm_sd_v14.ckpt"
else
    echo "mm_sd_v14.ckpt already exists, skipping download"
fi

if [ ! -f "models/Motion_Module/mm_sd_v15.ckpt" ]; then
    gdown "1ql0g_Ys4UCz2RnokYlBjyOYPbttbIpbu" -O "models/Motion_Module/mm_sd_v15.ckpt"
else
    echo "mm_sd_v15.ckpt already exists, skipping download"
fi

echo "Install finished!"

# Pause the script execution
read -p "Press any key to continue..." -n1 -s
