from pydub.effects import normalize
import os
from typing import List

from audio_file import AudioFile


def add_delay(file: AudioFile, suffix: str = 'delayed'):
    if not os.path.exists(file.file_path):
        raise Exception('Wooa cos nie dziala')

    if file.is_mp3:
        delayed_audio = file.silence + file.audio
        new_path = file.file_path[:-4] + f'_{suffix}.mp3'
        delayed_audio.export(new_path, format="mp3")
        return new_path


def normalize_volume(file: AudioFile, suffix: str = 'normalized'):
    if file.is_mp3 and file.audio:
        try:
            normalized_audio = normalize(file.audio)
            new_path = os.path.splitext(file.file_path)[0] + f'_{suffix}.mp3'
            normalized_audio.export(file.file_path, format="mp3")
            return new_path
        except Exception as e:
            print(f"Error normalizing {file.file_path}: {e}")
            return None


def merge_audio(file_1: AudioFile, file_2: AudioFile, suffix: str = 'merged'):
    if all([file_1.is_mp3, file_2.is_mp3, bool(file_1.audio), bool(file_2.audio)]):
        try:
            merged_audio = file_1.audio + file_2.audio
            new_path = os.path.splitext(file_1.file_path)[0] + f'_{suffix}.mp3'
            merged_audio.export(new_path, format="mp3")
            return new_path
        except Exception as e:
            print(f"Error normalizing {file_1.file_path}: {e}")
            return None


def scan_files(path: str) -> List[AudioFile]:
    audio_files = []
    for file in os.listdir(path):
        if file.endswith(('.mp4')):
            file_path = os.path.join(path, file)
            delay = 5
            audio_files.append(AudioFile(file_path, delay))
    return audio_files


def write_audio_files_to_python_file(audio_files: List[AudioFile], file_name: str):
    with open(file_name, 'w') as f:
        f.write("from audio_file_dt import AudioFile\n\n")
        for i, audio_file in enumerate(audio_files):
            f.write(f"audio_file{i} = AudioFile('{audio_file.file_path}', {audio_file.delay})\n")
        f.write("\n")
        f.write("all_audio_files = [")
        for i in range(len(audio_files)):
            if i > 0:
                f.write(", ")
            f.write(f"audio_file{i}")
        f.write("]\n")


def load_files():
    dir_path = 'O:\Downloads\quiz muzyczny'
    audio_files = scan_files(dir_path)
    write_audio_files_to_python_file(audio_files, 'main.py')
