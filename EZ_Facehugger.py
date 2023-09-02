import requests
import os

# Define the base URL for your Hugging Face repository
base_download_url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main"

file_urls = [
    f"{base_download_url}/text_encoder/config.json",
    f"{base_download_url}/text_encoder/model.fp16.safetensors",
    f"{base_download_url}/unet/config.json",
    f"{base_download_url}/unet/diffusion_pytorch_model.fp16.safetensors",
    f"{base_download_url}/vae/config.json",
    f"{base_download_url}/vae/diffusion_pytorch_model.fp16.safetensors",
    f"{base_download_url}/tokenizer/merges.txt",
    f"{base_download_url}/tokenizer/special_tokens_map.json",
    f"{base_download_url}/tokenizer/tokenizer_config.json",
    f"{base_download_url}/tokenizer/vocab.json",
    f"{base_download_url}/model_index.json"
]

script_directory = os.path.dirname(os.path.abspath(__file__))


local_file_paths = [
    "text_encoder/config.json",
    "text_encoder/model.fp16.safetensors",
    "unet/config.json",
    "unet/diffusion_pytorch_model.fp16.safetensors",
    "vae/config.json",
    "vae/diffusion_pytorch_model.fp16.safetensors",
    "tokenizer/merges.txt",
    "tokenizer/special_tokens_map.json",
    "tokenizer/tokenizer_config.json",
    "tokenizer/vocab.json",
    "model_index.json"
]

sd_root = "models/StableDiffusion/"

for file_path in local_file_paths:
    file_url = f"{base_download_url}/{file_path}"

    # Create the directory if it doesn't exist
    local_path = os.path.join(script_directory, sd_root, file_path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {local_path}")
    else:
        print(f"Failed to download: {file_url}")
