# pytaglib — WAV / Python

- **Pinned release:** `3.2.0`
- **License:** GPL-3.0-or-later
- **Parsed scope:** WAV header/audio metadata
- **Underlying family:** TagLib native WAV parser
- **Local input API:** `taglib.File(local path).sampleRate/channels/bitrate`
- **Documentation:** [API reference](<https://pypi.org/project/pytaglib/3.2.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bitrate": 128
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
