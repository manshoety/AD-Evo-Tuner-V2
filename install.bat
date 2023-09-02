@echo off
call conda activate adt

REM Download runwayml/StableDiffusion
echo Downloading runwayml/StableDiffusion...
python EZ_Facehugger.py

REM Download the motion modules
echo Downloading motion modules...
if not exist "models/Motion_Module/mm_sd_v14.ckpt" (
    gdown 1RqkQuGPaCO5sGZ6V6KZ-jUWmsRu48Kdq -O models/Motion_Module/mm_sd_v14.ckpt
) else (
	echo mm_sd_v14.ckpt already exists, skipping download
)

if not exist "models/Motion_Module/mm_sd_v15.ckpt" (
    gdown 1ql0g_Ys4UCz2RnokYlBjyOYPbttbIpbu -O models/Motion_Module/mm_sd_v15.ckpt
) else (
	echo mm_sd_v15.ckpt already exists, skipping download
)

echo Install finished!
pause
