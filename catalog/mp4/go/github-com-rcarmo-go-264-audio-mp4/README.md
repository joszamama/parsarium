# github.com/rcarmo/go-264/audio/mp4 — MP4 / Go

- **Pinned release:** `v0.0.0-20261008100743-cecca3835cbd`
- **License:** MIT
- **Parsed scope:** track count
- **Underlying family:** go-264 MP4 audio demuxer
- **Local input API:** `Open(context.Context, io.ReaderAt, size, Limits)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/rcarmo/go-264/audio/mp4@v0.0.0-20261008100743-cecca3835cbd>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_rcarmo_go_264_audio_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_rcarmo_go_264_audio_mp4
python3 parsarium.py run mp4 go github_com_rcarmo_go_264_audio_mp4 controls/mp4/red-av.mp4
```
