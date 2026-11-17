# github.com/gopxl/beep/v2/mp3 — MP3 / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v2.1.1`
- **License:** MIT
- **Parser family:** hajime/go-mp3 lineage via Beep
- **Local input API:** `Decode(io.ReadCloser) (beep.StreamSeekCloser, beep.Format, error); StreamSeekCloser.Stream, Len, Err`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gopxl/beep/v2/mp3@v2.1.1>)
- **Valid control:** [`controls/mp3/go-tone-44k-mono.mp3`](../../../../controls/mp3/go-tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control result](../../../../projects/mp3/go/github_com_gopxl_beep_v2_mp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "length_samples": 12672,
  "streamed_samples": 12672,
  "samples_sha256": "4c295234e0e6f8c8d269edeaf196553d1a921fbff3fbeb6ef9c273ee278ee8db"
}
```

## Run this target

```sh
python3 parsarium.py build mp3 go github_com_gopxl_beep_v2_mp3
python3 parsarium.py run mp3 go github_com_gopxl_beep_v2_mp3 controls/mp3/go-tone-44k-mono.mp3
```
