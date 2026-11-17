# mp3-parser — MP3 / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parser family:** biril mp3-parser JavaScript frame-header reader
- **Local input API:** `readFrame(DataView, offset, false) repeatedly over local Buffer-backed DataView; each result contains frame header and computed byte/sample lengths`
- **Documentation:** [API reference](<https://github.com/biril/mp3-parser/blob/19761d0aa0d88bcc215fd7fbeb197f8d00229bb4/README.md#readframeview-offset-requirenextframe>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control result](../../../../projects/mp3/javascript/mp3_parser/verification.json)

## Observed control result

```json
{
  "codec": "mp3",
  "mpeg_version_bits": "11",
  "layer": "Layer III",
  "sample_rate": 44100,
  "channels": 1,
  "bitrate": 64000,
  "frames": 11,
  "frame_bytes": 2298,
  "samples_per_frame": 1152,
  "total_samples": 12672,
  "header_variants": 1
}
```

## Run this target

```sh
python3 parsarium.py build mp3 javascript mp3_parser
python3 parsarium.py run mp3 javascript mp3_parser controls/mp3/tone-44k-mono.mp3
```
