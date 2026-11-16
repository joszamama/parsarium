# github.com/nareix/joy4/format/mp4 — MP4 / Go

- **Pinned release:** `v0.0.0-20200507095837-05a4ffbb5369`
- **License:** MIT
- **Parsed scope:** stream count
- **Underlying family:** joy4 MP4 lineage
- **Local input API:** `NewDemuxer(io.ReadSeeker).Streams()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/nareix/joy4/format/mp4@v0.0.0-20200507095837-05a4ffbb5369>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "streams": 2
}
```

Shared code lineage; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_nareix_joy4_format_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_nareix_joy4_format_mp4
python3 parsarium.py run mp4 go github_com_nareix_joy4_format_mp4 controls/mp4/red-av.mp4
```
