from dataclasses import dataclass, field

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment


@dataclass
class AudioFile:
    file_path: str
    delay: int = field(default=5)
    subtract: int = field(default=0)

    @property
    def is_mp4(self):
        return self.file_path.endswith('.mp4')

    @property
    def is_mp3(self):
        return self.file_path.endswith('.mp3')

    @property
    def audio(self):
        if self.is_mp3:
            audio = AudioSegment.from_mp3(self.file_path)
            if self.subtract > 0:
                audio = audio[self.subtract * 1000:]
            return audio

    @property
    def video(self):
        if self.is_mp4:
            return VideoFileClip(self.file_path)

    @property
    def silence(self):
        return AudioSegment.silent(duration=self.delay*1000)
