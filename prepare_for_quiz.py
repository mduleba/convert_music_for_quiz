from pydub.effects import normalize
import os
from typing import List

from audio_file_dt import AudioFile
from audio_files import all_audio_files


def convert_mp4_to_mp3(file: AudioFile):
    if file.is_mp4:
        new_name = file.file_path[:-4] + '.mp3'
        file.video.audio.write_audiofile(file.file_path[:-4] + '.mp3')
        return new_name


def add_delay(file: AudioFile, suffix: str = 'delayed'):
    if not os.path.exists(file.file_path):
        raise Exception('Wooa cos nie dziala')

    if file.is_mp3:
        delayed_audio = file.silence + file.audio
        new_path = file.file_path[:-4] + f'_{suffix}.mp3'
        delayed_audio.export(new_path, format="mp3")
        return new_path


def normalize_volume(file: AudioFile, suffix: str = 'normalized'):
    if file.is_mp3:
        normalized_audio = normalize(file.audio)
        new_path = file.file_path[:-4] + f'_{suffix}.mp3'
        normalized_audio.export(new_path, format="mp3")
        return new_path


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
    write_audio_files_to_python_file(audio_files, 'audio_files.py')


if __name__ == '__main__':
    results = []
    for file in all_audio_files:
        music_file = AudioFile(convert_mp4_to_mp3(file), file.delay, file.subtract)
        delayed_file = AudioFile(add_delay(music_file), 0, 0)
        normalized_file = AudioFile(normalize_volume(delayed_file), 0, 0)
        results.append(normalized_file)

