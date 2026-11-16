"""Read a valid ID3v2-tagged MP3 through one documented local-input API."""

import json
import os
import sys
from pathlib import Path


def tags(title, artist, album):
    return {"title": str(title).strip("\x00"), "artist": str(artist).strip("\x00"),
            "album": str(album).strip("\x00")}


def parse(name, path):
    if name == "mutagen":
        from mutagen.mp3 import MP3
        doc = MP3(path)
        return tags(doc.tags["TIT2"], doc.tags["TPE1"], doc.tags["TALB"])
    if name == "tinytag":
        from tinytag import TinyTag
        doc = TinyTag.get(path)
        return tags(doc.title, doc.artist, doc.album)
    if name == "pytaglib":
        import taglib
        with taglib.File(path) as doc:
            return tags(doc.tags["TITLE"][0], doc.tags["ARTIST"][0], doc.tags["ALBUM"][0])
    if name == "pymediainfo":
        from pymediainfo import MediaInfo
        tracks = MediaInfo.parse(path).tracks
        general = next(track for track in tracks if track.track_type == "General")
        audio = next(track for track in tracks if track.track_type == "Audio")
        return {**tags(general.title, general.performer, general.album),
                "sample_rate": int(audio.sampling_rate)}
    if name == "hachoir":
        from hachoir.parser import createParser
        doc = createParser(path)
        try:
            return {"description": doc.description}
        finally:
            doc.stream.close()
    if name == "pydub":
        from pydub import AudioSegment
        doc = AudioSegment.from_mp3(path)
        return {"sample_rate": doc.frame_rate, "channels": doc.channels,
                "duration_ms": len(doc)}
    if name == "soundfile":
        import soundfile
        doc = soundfile.info(path)
        return {"sample_rate": doc.samplerate, "channels": doc.channels,
                "frames": doc.frames, "format": doc.format}
    if name == "audioread":
        import audioread
        with audioread.audio_open(path) as doc:
            sample_bytes = sum(len(chunk) for chunk in doc)
            return {"sample_rate": doc.samplerate, "channels": doc.channels,
                    "duration_seconds": round(sample_bytes / (2 * doc.samplerate * doc.channels), 3)}
    if name == "librosa":
        import librosa
        samples, rate = librosa.load(path, sr=None)
        return {"sample_rate": rate, "samples": len(samples)}
    if name == "miniaudio":
        import miniaudio
        doc = miniaudio.mp3_read_f32(Path(path).read_bytes())
        return {"sample_rate": doc.sample_rate, "channels": doc.nchannels,
                "samples": len(doc.samples)}
    if name == "pygame":
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        import pygame
        pygame.mixer.init(frequency=8000, size=-16, channels=1)
        try:
            doc = pygame.mixer.Sound(path)
            return {"duration_ms": round(doc.get_length() * 1000)}
        finally:
            pygame.mixer.quit()
    if name == "av":
        import av
        with av.open(path) as doc:
            audio = doc.streams.audio[0]
            return {**tags(doc.metadata["title"], doc.metadata["artist"],
                           doc.metadata["album"]), "sample_rate": audio.codec_context.sample_rate}
    if name == "audiofile":
        import audiofile
        samples, rate = audiofile.read(path)
        return {"sample_rate": rate, "samples": len(samples)}
    if name == "audiomath":
        import audiomath
        doc = audiomath.Sound(path)
        return {"sample_rate": int(doc.fs), "samples": doc.nSamples}
    if name == "eyed3":
        import eyed3
        doc = eyed3.load(path)
        return tags(doc.tag.title, doc.tag.artist, doc.tag.album)
    if name == "mp3-tagger":
        from mp3_tagger import MP3File, VERSION_2
        doc = MP3File(str(path))
        doc.set_version(VERSION_2)
        return tags(doc.song, doc.artist, doc.album)
    if name == "music-tag":
        import music_tag
        doc = music_tag.load_file(path)
        return tags(doc["title"], doc["artist"], doc["album"])
    if name == "chemz":
        import chemz
        doc = chemz.read_track(Path(path))
        return {**tags(doc.title, doc.artist, doc.album), "sample_rate": doc.sample_rate}
    if name == "ffmpeg-python":
        import ffmpeg
        doc = ffmpeg.probe(path)
        return {**tags(doc["format"]["tags"]["title"], doc["format"]["tags"]["artist"],
                       doc["format"]["tags"]["album"]),
                "codec": doc["streams"][0]["codec_name"]}
    if name == "moviepy":
        from moviepy import AudioFileClip
        with AudioFileClip(path, fps=8000) as doc:
            return {"duration_seconds": round(doc.duration, 3),
                    "decoded_audio": bool(abs(doc.get_frame(0.123)[0]) > 0.01)}
    raise ValueError(f"unknown MP3 adapter: {name}")


if __name__ == "__main__":
    print(json.dumps(parse(sys.argv[1], sys.argv[2]), sort_keys=True))
