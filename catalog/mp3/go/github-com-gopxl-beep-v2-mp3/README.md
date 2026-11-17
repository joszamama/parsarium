# github.com/gopxl/beep/v2/mp3 — MP3 / Go

- **Pinned release:** `v2.1.1`
- **License:** MIT
- **Parsed scope:** decoded samples and sample rate
- **Underlying family:** hajime/go-mp3 via beep
- **Local input API:** `Decode(io.ReadCloser); Stream(samples)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gopxl/beep/v2/mp3@v2.1.1>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "samples": 16
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/go/github_com_gopxl_beep_v2_mp3/README.md)

```sh
python3 parsarium.py build mp3 go github_com_gopxl_beep_v2_mp3
python3 parsarium.py run mp3 go github_com_gopxl_beep_v2_mp3 controls/mp3_id3v2/tone-tags-44k.mp3
```
