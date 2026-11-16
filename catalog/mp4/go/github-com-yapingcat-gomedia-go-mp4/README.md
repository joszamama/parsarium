# github.com/yapingcat/gomedia/go-mp4 — MP4 / Go

- **Pinned release:** `v0.0.0-20240906162731-17feea57090c`
- **License:** MIT
- **Parsed scope:** track count
- **Underlying family:** gomedia MP4 lineage
- **Local input API:** `CreateMp4Demuxer(io.ReadSeeker).ReadHead()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/yapingcat/gomedia/go-mp4@v0.0.0-20240906162731-17feea57090c>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

Shared code lineage; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_yapingcat_gomedia_go_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_yapingcat_gomedia_go_mp4
python3 parsarium.py run mp4 go github_com_yapingcat_gomedia_go_mp4 controls/mp4/red-av.mp4
```
