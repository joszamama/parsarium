# php-ffmpeg/php-ffmpeg — WAV / PHP

- **Pinned release:** `v1.4.0`
- **License:** MIT
- **Parsed scope:** PCM16 codec, 8 kHz sample rate, mono channel count, 16-bit depth
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `FFProbe::create()->streams(local PCM WAV path)->audios()->first(); codec, sample rate, channels, bit depth`
- **Documentation:** [API reference](<https://github.com/PHP-FFMpeg/PHP-FFMpeg/blob/41fa00949ea2758cd34f076a8030df7198d57759/README.md>)
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

Official PHP-FFMpeg wrapper invokes local FFprobe 9.0.2; not an independent decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/php_ffmpeg_php_ffmpeg/README.md)

```sh
python3 parsarium.py build wav php php_ffmpeg_php_ffmpeg
python3 parsarium.py run wav php php_ffmpeg_php_ffmpeg controls/wav/256-samples.wav
```
