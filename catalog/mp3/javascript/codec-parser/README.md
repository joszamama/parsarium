# codec-parser — MP3 / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.5.0`
- **License:** LGPL-3.0-or-later
- **Parser family:** codec-parser JavaScript MPEG frame parser
- **Local input API:** `new CodecParser('audio/mpeg', { onCodecHeader }); parser.parseAll(Uint8Array) -> CodecFrame[] (header.sampleRate/channels/layer, samples, data, totalSamples)`
- **Documentation:** [API reference](<https://github.com/eshaz/codec-parser#readme>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control result](../../../../projects/mp3/javascript/codec_parser/verification.json)

## Observed control result

```json
{
  "codec": "mpeg",
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
python3 parsarium.py build mp3 javascript codec_parser
python3 parsarium.py run mp3 javascript codec_parser controls/mp3/tone-44k-mono.mp3
```
