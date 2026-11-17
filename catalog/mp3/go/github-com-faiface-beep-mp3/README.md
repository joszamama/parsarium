# github.com/faiface/beep/mp3 — MP3 / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.1.0`
- **License:** MIT
- **Parser family:** hajime/go-mp3 lineage via Beep
- **Local input API:** `Decode(io.ReadCloser) (beep.StreamSeekCloser, beep.Format, error); StreamSeekCloser.Stream, Len, Err`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/faiface/beep/mp3@v1.1.0>)
- **Valid control:** [`controls/mp3/go-tone-44k-mono.mp3`](../../../../controls/mp3/go-tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control result](../../../../projects/mp3/go/github_com_faiface_beep_mp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "length_samples": 12672,
  "streamed_samples": 12672,
  "samples_sha256": "99899cf5f832a09cd132845fb0e2a388e1f56d13388e769d2b6ffd6cee5091f5"
}
```

## Run this target

```sh
python3 parsarium.py build mp3 go github_com_faiface_beep_mp3
python3 parsarium.py run mp3 go github_com_faiface_beep_mp3 controls/mp3/go-tone-44k-mono.mp3
```
