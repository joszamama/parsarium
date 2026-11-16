# gemorroj/file-wav — WAV / PHP

- **Pinned release:** `2.3.2`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** PCM16 compression, 8 kHz sample rate, mono channel count, 32 ms duration
- **Underlying family:** Gemorroj FileWav native PHP WAV parser
- **Local input API:** `FileWav\Wav(local PCM WAV path)->getInfo(); compression, frame rate, channels, bits, length`
- **Documentation:** [API reference](<https://github.com/Gemorroj/FileWav/blob/9b3bfcb82d85d01681026d73575982a9d24fb484/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "compression": 1,
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16,
  "duration_seconds": 0.032
}
```

Dedicated WAV reader with its own header decoder; based on classAudioFile. No shared parser package in this cell.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/gemorroj_file_wav/README.md)

```sh
python3 parsarium.py build wav php gemorroj_file_wav
python3 parsarium.py run wav php gemorroj_file_wav controls/wav/256-samples.wav
```
