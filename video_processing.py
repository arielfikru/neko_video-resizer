import subprocess
import json
import torch
from utils import bytes_to_gb, get_file_size, check_ffmpeg

def resize_video(input_file, output_file, target_size_mb):
    if not check_ffmpeg():
        print("ffmpeg tidak terinstall. Menginstall ffmpeg...")
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True)
    
    original_size = get_file_size(input_file)
    original_size_gb = bytes_to_gb(original_size)
    print(f"Ukuran file asli: {original_size_gb:.2f} GB")

    probe = subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', input_file])
    video_info = json.loads(probe)
    
    width = int(video_info['streams'][0]['width'])
    height = int(video_info['streams'][0]['height'])
    
    new_width = int(width * 0.75)
    new_width = new_width - (new_width % 2)
    new_height = int(height * 0.75)
    new_height = new_height - (new_height % 2)

    duration = float(video_info['format']['duration'])
    target_bitrate = int((target_size_mb * 8 * 1024 * 1024) / duration)

    use_gpu = torch.cuda.is_available()
    if use_gpu:
        print("GPU tersedia. Menggunakan NVIDIA NVENC untuk encoding.")
        cmd = [
            "ffmpeg", "-i", input_file,
            "-c:v", "h264_nvenc",
            "-preset", "slow",
            "-crf", "23",
            "-maxrate", str(target_bitrate),
            "-bufsize", str(target_bitrate * 2),
            "-vf", f"scale={new_width}:{new_height}",
            "-c:a", "aac",
            "-b:a", "128k",
            output_file
        ]
    else:
        print("GPU tidak tersedia. Menggunakan CPU untuk encoding.")
        cmd = [
            "ffmpeg", "-i", input_file,
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "23",
            "-maxrate", str(target_bitrate),
            "-bufsize", str(target_bitrate * 2),
            "-vf", f"scale={new_width}:{new_height}",
            "-c:a", "aac",
            "-b:a", "128k",
            output_file
        ]

    subprocess.run(cmd, check=True)

    new_size = get_file_size(output_file)
    new_size_gb = bytes_to_gb(new_size)
    print(f"Ukuran file baru: {new_size_gb:.2f} GB")