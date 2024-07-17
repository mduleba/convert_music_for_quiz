
from dataclasses import dataclass, field
from functools import cached_property

from audio_file import AudioFile, AudioSilence
from youtube_video import YTVideo


class YTSongInterface:

    def get_audio_file(self) -> AudioFile:
        raise NotImplementedError()

    @property
    def audio_file(self):
        return self.get_audio_file()

    def download(self):
        raise NotImplementedError()


@dataclass
class YTDownloadedAudio(YTSongInterface):
    link: str

    delay: int = field(default=5)
    start: int = field(default=0)
    finish: int | None = field(default=None)

    video: YTVideo = field(init=False)

    def __post_init__(self):
        self.video = YTVideo(self.link)

    def get_audio_file(self):
        if self.video.converted and self.video.moved_to_media:
            return AudioFile(self.video.file_path, start=self.start, finish=self.finish)

    def download(self):
        self.video.download()
        self.video.copy_to_media()


@dataclass
class MergedYTAudio(YTSongInterface):
    yt_audios: list[YTDownloadedAudio]
    delay_between_songs: int = field(default=3)

    def validate(self):
        if len(self.yt_audios) < 2:
            raise TypeError()
        if not all([audio.video.moved_to_media for audio in self.yt_audios]):
            raise Exception("Files not loaded")

    @cached_property
    def count(self):
        return len(self.yt_audios)

    def get_audio_file(self):
        self.validate()
        audio_file = self.yt_audios[0].audio_file
        for i in range(1, self.count):
            audio_file = audio_file + AudioSilence(length=self.delay_between_songs) + self.yt_audios[i].audio_file
        return audio_file

    def download(self):
        for yt_audio in self.yt_audios:
            yt_audio.download()


