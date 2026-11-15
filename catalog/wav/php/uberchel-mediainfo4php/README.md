# uberchel/mediainfo4php — WAV / PHP

- **Pinned release:** `v1.0.8`
- **License:** MIT
- **Parsed scope:** PCM16 audio codec, 8 kHz mono sample stream, 128 kb/s audio bit rate
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `MediaInfo::Get(local PCM WAV path, false); audio codec, sample rate, channels, bit rate`
- **Documentation:** [API reference](<https://github.com/uberchel/MediaInfo4PHP/blob/f0a168902117e0094a90b94501f006965c9aabc2/ReadMe.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "audio_codec": "pcm_s16le",
  "sample_rate": "8000 Hz",
  "channels": "mono",
  "bit_rate": "128 kb/s"
}
```

MediaInfo4PHP wrapper invokes local FFmpeg 9.0.2; not the MediaInfoLib backend despite its name.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
