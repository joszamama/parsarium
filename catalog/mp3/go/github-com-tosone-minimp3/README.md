# github.com/tosone/minimp3 — MP3 / Go

- **Pinned release:** `v1.1.0`
- **License:** MIT
- **Parsed scope:** decoded PCM bytes and audio format
- **Underlying family:** minimp3 decoder
- **Local input API:** `DecodeFull([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tosone/minimp3@v1.1.0>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "decoded_bytes": 94464
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/go/github_com_tosone_minimp3/README.md)

```sh
python3 parsarium.py build mp3 go github_com_tosone_minimp3
python3 parsarium.py run mp3 go github_com_tosone_minimp3 controls/mp3_id3v2/tone-tags-44k.mp3
```
