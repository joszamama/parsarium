# audiostreamify/hvap — WAV / PHP

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** RIFF/WAVE PCM16 format, 8 kHz sample rate, mono channel count
- **Underlying family:** getID3 native RIFF/WAVE parser
- **Local input API:** `Processor::audio(local PCM WAV path)->analyze(); fileformat and audio sample rate/channels/bit depth`
- **Documentation:** [API reference](<https://github.com/audiostreamify/hvap/blob/e9c0c63e9d7ed13f03b152c01452008b2076fc96/src/Mocks/ID3Tags.php>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "fileformat": "wav",
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16
}
```

Audio path delegates to pinned getID3; separate Composer package path, same parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/audiostreamify_hvap/README.md)

```sh
python3 parsarium.py build wav php audiostreamify_hvap
python3 parsarium.py run wav php audiostreamify_hvap controls/wav/256-samples.wav
```
