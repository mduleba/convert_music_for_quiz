from audio_file import AudioFile, AudioSilence
from youtube_video import YTVideo
import os

from yt_downloaded_audio import YTDownloadedAudio, MergedYTAudio

sound_effects = [
    YTDownloadedAudio('https://www.youtube.com/watch?v=uwTQn0aT9zs'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=OOh2SAdDh34'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=NgEL0We444M'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=c7JrVrGwGNE'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=BxVh7T41GAI'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=wD41SxG3rgs'),
    MergedYTAudio([YTDownloadedAudio('https://www.youtube.com/watch?v=wRG766JTT08'), YTDownloadedAudio('https://www.youtube.com/watch?v=wRG766JTT08')]),
    YTDownloadedAudio('https://www.youtube.com/watch?v=tVPBOHHe9Jk', start=20, finish=49),
    YTDownloadedAudio('https://www.youtube.com/watch?v=ar5kdSneOhk'),
    MergedYTAudio([YTDownloadedAudio('https://www.youtube.com/watch?v=sOZDenFamKY'), YTDownloadedAudio('https://www.youtube.com/watch?v=sOZDenFamKY')]),
    MergedYTAudio([YTDownloadedAudio('https://www.youtube.com/watch?v=UfhR-oEk4EA'), YTDownloadedAudio('https://www.youtube.com/watch?v=i7oHvzfDSW4')]),
    MergedYTAudio([YTDownloadedAudio('https://www.youtube.com/watch?v=jtKY1xI3M6c'), YTDownloadedAudio('https://www.youtube.com/watch?v=7sCcE2Fob4U')]),
    YTDownloadedAudio('https://www.youtube.com/watch?v=DfYInNvYyFA'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=MXibe4aNdGg'),
    MergedYTAudio([YTDownloadedAudio('https://www.youtube.com/watch?v=Y-PeeTaVvns'), YTDownloadedAudio('https://www.youtube.com/watch?v=Y-PeeTaVvns')]),
    MergedYTAudio([YTDownloadedAudio('https://www.youtube.com/watch?v=gxfyQnd-0ew'), YTDownloadedAudio('https://www.youtube.com/watch?v=gxfyQnd-0ew')]),
    YTDownloadedAudio('https://www.youtube.com/watch?v=ISzpadnuZ10'),
]

themes = [
    YTDownloadedAudio('https://www.youtube.com/watch?v=FDqXO7XOw7c'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=Vofkw9-O18c'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=RUN6Kqd9xgs'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=zLdAURdn4o4'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=Ekq3TDPznGI'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=FZTvUIMcT40'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=Hl5xbFXrFU4'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=F2_pg8xd1To'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=R5hCkh2AH58'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=4lX2iP6uL_I'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=5p1vacn3KcE'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=Ze38kD1ZNfo'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=-VQQCI5C-co'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=F5-XnZZvXqY'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=ubWL8VAPoYw'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=Lyi2tT3tiPU'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=xLhUGq1nhdU'),
    YTDownloadedAudio('https://www.youtube.com/watch?v=0Mp48W8j2jA'),
]

songs = [
    YTDownloadedAudio('https://www.youtube.com/watch?v=aw2Z68-atbc', finish=40),
]

if __name__ == '__main__':
    results = []
    for song in songs:
        try:
            song.download()
            audio_file = song.get_audio_file()
            audio_file.audio = AudioSilence().audio + audio_file.audio
            audio_file.save()
            results.append(audio_file)
        except Exception as e:
            print(song)
