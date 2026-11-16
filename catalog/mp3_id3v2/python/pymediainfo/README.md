# pymediainfo — MP3 with ID3v2 / Python

- **Pinned release:** `7.0.1`
- **License:** MIT
- **Parsed scope:** ID3v2 tags and MP3 sample rate
- **Underlying family:** MediaInfo native MP3 parser
- **Local input API:** `pymediainfo.MediaInfo.parse(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pymediainfo/7.0.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "sample_rate": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
