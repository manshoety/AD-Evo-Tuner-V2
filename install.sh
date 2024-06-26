#!/bin/bash

# Locate the conda binary
CONDA_BIN=$(which conda)

# If conda is not found, exit
if [ -z "$CONDA_BIN" ]; then
    echo "Conda is not found in PATH."
    exit 1
fi

# Infer the possible location of conda.sh based on the location of the conda binary
CONDA_SH=$(dirname "$CONDA_BIN")/../etc/profile.d/conda.sh

# Source conda.sh if it exists
if [ -f "$CONDA_SH" ]; then
    source "$CONDA_SH"
else
    echo "Could not find conda.sh script."
    exit 2
fi

# activate the conda environment
conda activate ADT

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "Error activating conda environment"
    exit 1
fi

# Download runwayml/StableDiffusion
echo "Downloading runwayml/StableDiffusion..."
python EZ_Facehugger.py

# Check python script status
if [ $? -ne 0 ]; then
    echo "Error running EZ_Facehugger.py"
    exit 2
fi

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
