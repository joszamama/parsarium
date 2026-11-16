# github.com/tetsuo/mp4 — MP4 / Go

- **Pinned release:** `v0.3.0`
- **License:** MIT
- **Parsed scope:** ftyp brand only
- **Underlying family:** tetsuo MP4 box reader
- **Local input API:** `NewReader([]byte).Next(); ReadFtyp([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tetsuo/mp4@v0.3.0>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/github_com_tetsuo_mp4/README.md)

```sh
python3 parsarium.py build mp4 go github_com_tetsuo_mp4
python3 parsarium.py run mp4 go github_com_tetsuo_mp4 controls/mp4/red-av.mp4
```
