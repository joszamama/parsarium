# github.com/tcolgate/mp3 — MP3 / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20170426193717-e79c5a46d300`
- **License:** MIT
- **Parser family:** tcolgate/mp3 frame parser
- **Local input API:** `NewDecoder(io.Reader); Decoder.Decode(*Frame,*int); Frame.Header/Size/Samples`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tcolgate/mp3@v0.0.0-20170426193717-e79c5a46d300>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control result](../../../../projects/mp3/go/github_com_tcolgate_mp3/verification.json)

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
python3 parsarium.py build mp3 go github_com_tcolgate_mp3
python3 parsarium.py run mp3 go github_com_tcolgate_mp3 controls/mp3/tone-44k-mono.mp3
```
