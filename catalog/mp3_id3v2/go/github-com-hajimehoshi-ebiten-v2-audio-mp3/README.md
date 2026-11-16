# github.com/hajimehoshi/ebiten/v2/audio/mp3 — MP3 with ID3v2 / Go

- **Pinned release:** `v2.10.6`
- **License:** Apache-2.0
- **Parsed scope:** decoded PCM bytes and sample rate
- **Underlying family:** hajime/go-mp3 lineage
- **Local input API:** `DecodeWithoutResampling(io.Reader); Read([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hajimehoshi/ebiten/v2/audio/mp3@v2.10.6>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "decoded_bytes": 64
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/go/github_com_hajimehoshi_ebiten_v2_audio_mp3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 go github_com_hajimehoshi_ebiten_v2_audio_mp3
python3 parsarium.py run mp3_id3v2 go github_com_hajimehoshi_ebiten_v2_audio_mp3 controls/mp3_id3v2/tone-tags-44k.mp3
```
