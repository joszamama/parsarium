"""Run one pinned Python WAV API against the valid four-sample PCM control."""

import json
import struct
import sys
from pathlib import Path


def samples(rate, channels, values):
    out = []
    for value in values:
        value = float(value)
        out.append(round(value * 32768) if -1 <= value <= 1 and not value.is_integer()
                   else round(value))
    return {"sample_rate": int(rate), "channels": int(channels), "samples": out}


def info(rate, channels, bits):
    return {"sample_rate": int(rate), "channels": int(channels),
            "bits_per_sample": int(bits)}


def run(name: str, path: Path):
    if name == "scipy":
        from scipy.io import wavfile
        rate, data = wavfile.read(str(path))
        return samples(rate, 1, data)
    if name == "soundfile":
        import soundfile
        data, rate = soundfile.read(str(path))
        return samples(rate, 1, data)
    if name == "librosa":
        import librosa
        data, rate = librosa.load(str(path), sr=None)
        return samples(rate, 1, data)
    if name == "audioread":
        import audioread
        with audioread.audio_open(str(path)) as reader:
            raw = b"".join(reader)
            data = struct.unpack("<" + "h" * (len(raw) // 2), raw)
            return samples(reader.samplerate, reader.channels, data)
    if name == "pydub":
        from pydub import AudioSegment
        audio = AudioSegment.from_wav(str(path))
        return samples(audio.frame_rate, audio.channels, audio.get_array_of_samples())
    if name == "miniaudio":
        import miniaudio
        audio = miniaudio.wav_read_f32(path.read_bytes())
        return samples(audio.sample_rate, audio.nchannels, audio.samples)
    if name == "wavio":
        import wavio
        audio = wavio.read(str(path))
        return samples(audio.rate, audio.data.shape[1], audio.data[:, 0])
    if name == "wavfile":
        import wavfile
        data, rate, _bits = wavfile.read(str(path))
        return samples(rate, 1, (row[0] for row in data))
    if name == "tinytag":
        from tinytag import TinyTag
        tag = TinyTag.get(str(path))
        return {"sample_rate": int(tag.samplerate), "channels": int(tag.channels),
                "duration_seconds": tag.duration}
    if name == "mutagen":
        from mutagen.wave import WAVE
        wave = WAVE(str(path))
        return info(wave.info.sample_rate, wave.info.channels, wave.info.bits_per_sample)
    if name == "waveinfo":
        from waveinfo import WavFile
        wave = WavFile(str(path))
        return {**info(wave.detail.sample_rate, wave.detail.channels, wave.detail.bit_depth),
                "sample_frames": wave.raw_details.total_samples}
    if name == "audiomath":
        import audiomath
        audio = audiomath.Sound(str(path))
        return samples(audio.fs, audio.nChannels, audio.y[:, 0])
    if name == "riffy":
        from riffy import WAVParser
        wave = WAVParser(str(path))
        return {**info(wave.format_info.sample_rate, wave.format_info.channels,
                       wave.format_info.bits_per_sample),
                "samples": list(struct.unpack("<4h", wave.audio_data))}
    if name == "pygame":
        import pygame
        pygame.mixer.init(frequency=8000, size=-16, channels=1)
        try:
            audio = pygame.mixer.Sound(str(path))
            return samples(8000, 1, struct.unpack("<4h", audio.get_raw()))
        finally:
            pygame.mixer.quit()
    if name == "av":
        import av
        with av.open(str(path)) as container:
            stream = container.streams.audio[0]
            values = [int(value) for frame in container.decode(audio=0)
                      for value in frame.to_ndarray().ravel()]
            return samples(stream.sample_rate, stream.channels, values)
    if name == "audiofile":
        import audiofile
        data, rate = audiofile.read(str(path))
        return samples(rate, 1, data)
    if name == "pymediainfo":
        from pymediainfo import MediaInfo
        media = MediaInfo.parse(str(path))
        audio = next(track for track in media.tracks if track.track_type == "Audio")
        return {"sample_rate": int(audio.sampling_rate), "channels": int(audio.channel_s)}
    if name == "hachoir":
        from hachoir.parser import createParser
        parser = createParser(str(path))
        wave = parser["format"]
        return info(wave["sample_per_sec"].value, wave["nb_channel"].value,
                    wave["bit_per_sample"].value)
    if name == "pytaglib":
        import taglib
        with taglib.File(str(path)) as audio:
            return {"sample_rate": audio.sampleRate, "channels": audio.channels,
                    "bitrate": audio.bitrate}
    if name == "audiolab":
        from audiolab import load_audio
        data, rate = load_audio(str(path))
        return samples(rate, data.shape[0], data[0])
    if name == "simpleaudio":
        import simpleaudio
        audio = simpleaudio.WaveObject.from_wave_file(str(path))
        return samples(audio.sample_rate, audio.num_channels,
                       struct.unpack("<4h", audio.audio_data))
    raise ValueError(f"unknown package: {name}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: main.py PACKAGE CONTROL_PATH")
    print(json.dumps(run(sys.argv[1], Path(sys.argv[2]))))
