# github.com/abema/go-mp4 — MP4 / Go

- **Pinned release:** `v1.7.4`
- **License:** MIT
- **Parsed scope:** movie box
- **Underlying family:** go-mp4 box parser
- **Local input API:** `ExtractBox(io.ReadSeeker, BoxPath{moov})`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/abema/go-mp4@v1.7.4>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "moov_size": 1442
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/go/abema_go_mp4/README.md)

```sh
python3 parsarium.py build mp4 go abema_go_mp4
python3 parsarium.py run mp4 go abema_go_mp4 controls/mp4/red-av.mp4
```
