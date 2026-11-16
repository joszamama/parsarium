# waveinfo — WAV / Python

- **Pinned release:** `0.5.0`
- **License:** MIT
- **Parsed scope:** WAV header/audio metadata
- **Underlying family:** waveinfo RIFF/WAV parser
- **Local input API:** `waveinfo.WavFile(local path).detail and raw_details`
- **Documentation:** [API reference](<https://pypi.org/project/waveinfo/0.5.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16,
  "sample_frames": 4
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/python/waveinfo/README.md)

```sh
python3 parsarium.py build wav python waveinfo
python3 parsarium.py run wav python waveinfo controls/wav/four-samples.wav
```
