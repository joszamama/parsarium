# github.com/hajimehoshi/go-mp3 — MP3 / Go

- **Pinned release:** `v0.3.4`
- **License:** Apache-2.0
- **Parsed scope:** decoded PCM bytes and sample rate
- **Underlying family:** hajime/go-mp3 lineage
- **Local input API:** `NewDecoder(io.Reader); Read([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hajimehoshi/go-mp3@v0.3.4>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone-44k.mp3`](../../../../controls/mp3/id3v2-tagged-tone-44k.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "decoded_bytes": 64
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/go/github_com_hajimehoshi_go_mp3/README.md)

```sh
python3 parsarium.py build mp3 go github_com_hajimehoshi_go_mp3
python3 parsarium.py run mp3 go github_com_hajimehoshi_go_mp3 controls/mp3/id3v2-tagged-tone-44k.mp3
```
