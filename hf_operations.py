import os
import requests
from huggingface_hub import HfApi

def download_from_hf(url, filename, token):
    if os.path.exists(filename):
        print(f"File {filename} sudah ada. Melewati proses download.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"File berhasil diunduh: {filename}")

def upload_to_hf(filename, repo_id, token):
    api = HfApi()
    api.upload_file(
        path_or_fileobj=filename,
        path_in_repo=filename,
        repo_id=repo_id,
        token=token,
        repo_type="dataset"
    )
    print(f"File berhasil diunggah: {filename}")