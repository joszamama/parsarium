# github.com/dmulholl/mp3lib — MP3 / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.0.0`
- **License:** Unlicense
- **Parser family:** dmulholl/mp3lib frame parser
- **Local input API:** `NextFrame(io.Reader) *MP3Frame; MP3Frame header and frame fields`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/dmulholl/mp3lib@v1.0.0>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control result](../../../../projects/mp3/go/github_com_dmulholl_mp3lib/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "frame_bytes": 2298,
  "samples_per_frame": 1152,
  "bitrate": 64000
}
```

## Run this target

```sh
python3 parsarium.py build mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py run mp3 go github_com_dmulholl_mp3lib controls/mp3/tone-44k-mono.mp3
```
