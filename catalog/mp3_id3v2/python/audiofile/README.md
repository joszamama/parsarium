# audiofile — MP3 with ID3v2 / Python

- **Pinned release:** `1.6.1`
- **License:** MIT
- **Parsed scope:** decoded PCM sample count
- **Underlying family:** audiofile via soundfile/libsndfile
- **Local input API:** `audiofile.read(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/audiofile/1.6.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "samples": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
