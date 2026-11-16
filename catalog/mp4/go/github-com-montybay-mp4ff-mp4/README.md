# github.com/montybay/mp4ff/mp4 — MP4 / Go

- **Pinned release:** `v0.0.0-20261017003302-c9570d1e4b3c`
- **License:** MIT, MIT
- **Parsed scope:** brand and track count
- **Underlying family:** mp4ff lineage
- **Local input API:** `DecodeFile(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/montybay/mp4ff/mp4@v0.0.0-20261017003302-c9570d1e4b3c>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom",
  "tracks": 2
}
```

Shared code lineage; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_montybay_mp4ff_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_montybay_mp4ff_mp4
python3 parsarium.py run mp4 go github_com_montybay_mp4ff_mp4 controls/mp4/red-av.mp4
```
