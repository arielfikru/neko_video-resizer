import os
import subprocess

def bytes_to_gb(bytes_size):
    return bytes_size / (1024 * 1024 * 1024)

def get_file_size(filename):
    return os.path.getsize(filename)

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False