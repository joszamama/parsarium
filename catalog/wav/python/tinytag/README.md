# tinytag — WAV / Python

- **Pinned release:** `2.3.2`
- **License:** MIT
- **Parsed scope:** WAV header/audio metadata
- **Underlying family:** tinytag RIFF/WAV metadata parser
- **Local input API:** `tinytag.TinyTag.get(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/tinytag/2.3.2/>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "duration_seconds": 0.0005
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
