# github.com/mattetti/audio/mp3 — MP3 with ID3v2 / Go

- **Pinned release:** `v0.0.0-20240411020228-c5379f9b5b61`
- **License:** MIT
- **Parsed scope:** reported duration and frame count
- **Underlying family:** tcolgate MP3 frame lineage
- **Local input API:** `NewDecoder(io.Reader).Duration()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/mattetti/audio/mp3@v0.0.0-20240411020228-c5379f9b5b61>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "duration_ms": 1071,
  "frames": 42
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/go/github_com_mattetti_audio_mp3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 go github_com_mattetti_audio_mp3
python3 parsarium.py run mp3_id3v2 go github_com_mattetti_audio_mp3 controls/mp3_id3v2/tone-tags-44k.mp3
```
