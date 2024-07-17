from __future__ import annotations

import os
from dataclasses import dataclass, field
from pydub.effects import normalize

from pydub import AudioSegment
import ntpath


class AudioInterface:
    audio: AudioSegment
    name: str

    def __add__(self, other: AudioInterface):
        if isinstance(other, AudioInterface):
            self.audio += other.audio
            return self
        else:
            raise TypeError()


@dataclass
class AudioFile(AudioInterface):
    file_path: str
    start: int = field(default=0)
    finish: int | None = field(default=None)

    normalize: bool = field(default=True)

    audio: AudioSegment = field(init=False)

    def get_audio(self):
        if not self.is_mp3:
            raise TypeError()

        audio = AudioSegment.from_mp3(self.file_path)
        if self.start > 0:
            audio = audio[self.start * 1000:]
            self.file_path = self.without_extension + f"_from_{self.start}.mp3"

        if self.finish:
            audio = audio[:self.finish * 1000]
            self.file_path = self.without_extension + f"_to_{self.finish}.mp3"

        if self.normalize:
            audio = normalize(audio)
            self.file_path = self.without_extension + "_normalized.mp3"
        return audio

    def __post_init__(self):
        try:
            self.audio = self.get_audio()
        except Exception as e:
            print(f"Error while geting audio: {self.file_path} - {e}")

    @property
    def is_mp3(self):
        return self.file_path.endswith('.mp3')

    @property
    def name(self):
        return ntpath.basename(self.file_path)

    @property
    def without_extension(self):
        return os.path.splitext(self.file_path)[0]

    def save(self):
        self.audio.export(self.file_path, format="mp3")


@dataclass
class AudioSilence(AudioInterface):
    name: str = field(default="delay")
    length: int = field(default=5)

    @property
    def audio(self):
        return AudioSegment.silent(duration=self.length*1000)

