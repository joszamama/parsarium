# protonemedia/php-ffmpeg — WAV / PHP

- **Pinned release:** `v1.2.0`
- **License:** MIT
- **Parsed scope:** PCM16 codec, 8 kHz sample rate, mono channel count, 16-bit depth
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `FFProbe::create()->streams(local PCM WAV path)->audios()->first(); codec, sample rate, channels, bit depth`
- **Documentation:** [API reference](<https://github.com/protonemedia/PHP-FFMpeg/blob/4c52b1ce23b9980795dedc95a7958d972b47ada5/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "codec": "pcm_s16le",
  "sample_rate": "8000",
  "channels": 1,
  "bits_per_sample": 16
}
```

Protonemedia fork of PHP-FFMpeg, distinct source ref; local FFprobe 9.0.2 is the shared underlying parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/protonemedia_php_ffmpeg/README.md)

```sh
python3 parsarium.py build wav php protonemedia_php_ffmpeg
python3 parsarium.py run wav php protonemedia_php_ffmpeg controls/wav/256-samples.wav
```
