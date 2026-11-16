# mhor/php-mediainfo — WAV / PHP

- **Pinned release:** `5.8.0`
- **License:** MIT
- **Parsed scope:** PCM format, 8 kHz sample rate, mono channel count, 16-bit depth
- **Underlying family:** MediaInfoLib native RIFF/WAVE parser
- **Local input API:** `MediaInfo::getInfo(local PCM WAV path); first audio track format, sampling_rate, channel_s, bit_depth`
- **Documentation:** [API reference](<https://github.com/mhor/php-mediainfo/blob/a0be4ef4dc1f56292793ad31c2b3efc75bfdbf05/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/32768-samples.wav`](../../../../controls/wav/32768-samples.wav)

## Observed control result

```json
{
  "format": "PCM",
  "sample_rate": 8000,
  "channels": 1,
  "bit_depth": 16
}
```

Composer wrapper delegates to external MediaInfo 26.10 CLI; same release lock as the PHP MP3 cell. The 65,580-byte control satisfies the CLI read buffer.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/mhor_php_mediainfo/README.md)

```sh
python3 parsarium.py build wav php mhor_php_mediainfo
python3 parsarium.py run wav php mhor_php_mediainfo controls/wav/32768-samples.wav
```
