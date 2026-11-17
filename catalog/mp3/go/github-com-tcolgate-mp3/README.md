# github.com/tcolgate/mp3 — MP3 / Go

- **Pinned release:** `v0.0.0-20170426193717-e79c5a46d300`
- **License:** MIT
- **Parsed scope:** MPEG frame size and samples
- **Underlying family:** tcolgate MP3 frame lineage
- **Local input API:** `NewDecoder(io.Reader).Decode(*Frame,*int)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tcolgate/mp3@v0.0.0-20170426193717-e79c5a46d300>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone-44k.mp3`](../../../../controls/mp3/id3v2-tagged-tone-44k.mp3)

## Observed control result

```json
{
  "frame_bytes": 208,
  "samples": 1152
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/go/github_com_tcolgate_mp3/README.md)

```sh
python3 parsarium.py build mp3 go github_com_tcolgate_mp3
python3 parsarium.py run mp3 go github_com_tcolgate_mp3 controls/mp3/id3v2-tagged-tone-44k.mp3
```
