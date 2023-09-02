#!/bin/bash

# Locate the conda binary
CONDA_BIN=$(which conda)

# If conda is not found, exit
if [ -z "$CONDA_BIN" ]; then
    echo "Conda is not found in PATH."
    exit 1
fi

# Infer the possible location of conda.sh based on the location of the conda binary
CONDA_SH=$(realpath $(dirname "$CONDA_BIN")/../etc/profile.d/conda.sh)

# Source conda.sh if it exists
if [ -f "$CONDA_SH" ]; then
    source "$CONDA_SH"
else
    echo "Could not find conda.sh script."
    exit 2
fi

# activate the conda environment
conda activate ADT

# Check if environment activation was successful
if [ $? -ne 0 ]; then
    echo "Failed to activate conda environment."
    exit 3
fi

# run the python script
python ez-adt_v0.py
