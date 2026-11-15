# char0n/ffmpeg-php — WAV / PHP

- **Pinned release:** `3.2.2`
- **License:** BSD-3-Clause
- **Parsed scope:** PCM16 audio codec, 8 kHz mono audio, rounded 30 ms duration
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `Movie(local PCM WAV path); audio codec, sample rate, channels, duration`
- **Documentation:** [API reference](<https://github.com/char0n/ffmpeg-php/blob/9a38fdc2a3b2bf2d5df9d28a571f05a1e71c0cf8/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "audio_codec": "pcm_s16le",
  "sample_rate": 8000,
  "channels": 1,
  "duration_seconds": 0.03
}
```

FFmpegPHP wrapper parses local WAV via FFprobe 9.0.2; duration rounds to hundredths.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
