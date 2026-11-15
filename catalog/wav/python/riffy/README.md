# riffy — WAV / Python

- **Pinned release:** `0.3.16`
- **License:** MIT
- **Parsed scope:** PCM samples
- **Underlying family:** riffy RIFF/WAV parser
- **Local input API:** `riffy.WAVParser(local path).format_info and audio_data`
- **Documentation:** [API reference](<https://pypi.org/project/riffy/0.3.16/>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
