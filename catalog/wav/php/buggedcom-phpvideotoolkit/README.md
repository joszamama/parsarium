# buggedcom/phpvideotoolkit — WAV / PHP

- **Pinned release:** `2.2.5`
- **License:** MIT
- **Parsed scope:** 8 kHz mono PCM signed 16-bit WAV audio
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `PHPVideoToolkit\MediaParser::getFileInformation(local PCM WAV path); audio sample rate, channel count, codec`
- **Documentation:** [API reference](<https://github.com/buggedcom/phpvideotoolkit-v2/blob/383a5b2c0ee7f4de4efea9a9154bb693630bbe0f/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "codec": "pcm_s16le"
}
```

Composer wrapper delegates to local FFmpeg 9.0.2; same release lock as the PHP MP3 cell.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
