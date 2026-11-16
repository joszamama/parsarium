# hachoir — MP3 with ID3v2 / Python

- **Pinned release:** `3.4.0`
- **License:** GPL-2.0-only
- **Parsed scope:** MPEG audio frame description
- **Underlying family:** Hachoir MPEG audio parser
- **Local input API:** `hachoir.parser.createParser(local path)`
- **Documentation:** [API reference](<https://hachoir.readthedocs.io/en/latest/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "description": "MPEG-2.5 layer III, 32.0 Kbit/sec, 8.0 kHz, Single channel"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
