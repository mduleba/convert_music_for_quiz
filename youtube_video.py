from functools import cached_property
import os
from dataclasses import dataclass, field
import shutil
import subprocess
import pytube
import yt_dlp


@dataclass
class YTVideo:
    url: str

    file_path: str = field(default="")
    converted: bool = field(default=False)
    moved_to_media: bool = field(default=False)

    @property
    def file_name(self):
        directory, file_name = self.file_path.rsplit("\\", 1)
        return file_name

    @cached_property
    def video_info(self):
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(self.url, download=False)

    @property
    def title(self):
        return self.video_info['title']

    @property
    def author(self):
        return self.video_info['uploader']

    def wait_until_file(self):
        while True:
            if self.file_path:
                break

    def download(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'tmp/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=True)
            self.file_path = ydl.prepare_filename(info_dict).rsplit('.', 1)[0] + '.mp3'
        self.wait_until_file()
        self.converted = True

    def convert_to_mp3(self):
        assert self.file_path, 'download first'
        assert not self.converted, 'already converted'

        try:
            new_path = os.path.splitext(self.file_path)[0] + '.mp3'
            # Use ffmpeg to ensure correct conversion
            subprocess.run([
                'ffmpeg', '-i', self.file_path, '-q:a', '0', new_path
            ], check=True)
            os.remove(self.file_path)  # Remove the original file after conversion
            self.wait_until_file()
            self.file_path = new_path
            self.converted = True
        except Exception as e:
            print(f"Error converting {self.file_path}: {e}")

    def delete(self):
        assert self.file_path, 'nothing to delete'
        os.remove(self.file_path)
        self.file_path = ""

    def copy_to_media(self, media_path='C:\\Users\\Megacake\\PycharmProjects\\sound-video-tools\\media\\songs\\'):

        src_path = self.file_path
        dst_path = os.path.join(media_path, self.file_name)
        shutil.move(src_path, dst_path)
        self.file_path = dst_path
        self.moved_to_media = True


if __name__ == '__main__':
    billie_jean = YTVideo("https://www.youtube.com/watch?v=Zi_XLOBDo_Y")
    billie_jean.download()
    billie_jean.copy_to_media()