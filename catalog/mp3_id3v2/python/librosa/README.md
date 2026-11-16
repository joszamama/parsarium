# librosa — MP3 with ID3v2 / Python

- **Pinned release:** `1.0.0`
- **License:** ISC
- **Parsed scope:** decoded PCM sample count
- **Underlying family:** librosa via soundfile/libsndfile
- **Local input API:** `librosa.load(local path, sr=None)`
- **Documentation:** [API reference](<https://librosa.org/doc/main/api/generated/librosa.load.html>)
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
