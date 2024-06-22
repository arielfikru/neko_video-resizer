import argparse
import os
from hf_operations import download_from_hf, upload_to_hf
from video_processing import resize_video

def main():
    parser = argparse.ArgumentParser(description="Resize video dengan target ukuran tertentu.")
    parser.add_argument("input", help="Path file input lokal atau URL Hugging Face")
    parser.add_argument("output", help="Nama file output")
    parser.add_argument("--target_size", type=int, default=1000, help="Target ukuran file dalam MB (default: 1000)")
    parser.add_argument("--hf_token", help="Token Hugging Face (diperlukan jika menggunakan URL Hugging Face)")
    parser.add_argument("--repo_id", help="ID repository Hugging Face untuk upload (opsional)")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    target_size_mb = args.target_size
    hf_token = args.hf_token
    repo_id = args.repo_id

    if input_file.startswith("https://huggingface.co/"):
        if not hf_token:
            raise ValueError("Token Hugging Face diperlukan untuk mengunduh dari URL Hugging Face")
        local_input = os.path.basename(input_file)
        print(f"Mengunduh file dari Hugging Face: {input_file}")
        download_from_hf(input_file, local_input, hf_token)
        input_file = local_input

    print(f"Memulai proses resize video dengan target ukuran {target_size_mb} MB...")
    resize_video(input_file, output_file, target_size_mb)

    if repo_id and hf_token:
        print(f"Mengunggah file hasil ke Hugging Face repository: {repo_id}")
        upload_to_hf(output_file, repo_id, hf_token)

    print("Proses selesai.")

if __name__ == "__main__":
    main()