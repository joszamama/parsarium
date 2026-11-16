# hachoir — WAV / Python

- **Pinned release:** `3.4.0`
- **License:** GPL-2.0-only
- **Parsed scope:** WAV header/audio metadata
- **Underlying family:** Hachoir RIFF/WAV parser
- **Local input API:** `hachoir.parser.createParser(local path)["format"]`
- **Documentation:** [API reference](<https://hachoir.readthedocs.io/en/latest/>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
