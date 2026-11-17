# libmad — MP3 / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.16.5`
- **License:** GPL-2.0-or-later
- **Parser family:** libmad MPEG audio decoder
- **Local input API:** `mad_stream_buffer(stream, local bytes followed by MAD_BUFFER_GUARD zero bytes, length); mad_frame_decode() until MAD_ERROR_BUFLEN; mad_synth_frame(); MAD_RECOVERABLE() error classification`
- **Documentation:** [API reference](<https://codeberg.org/tenacityteam/libmad/src/tag/0.16.5/include/mad.h.in>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control result](../../../../projects/mp3/c/libmad/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "layer": 3,
  "frames": 11,
  "decoded_samples": 12672,
  "bit_rate_min": 64000,
  "bit_rate_max": 64000,
  "recoverable_errors": 0,
  "consumed_bytes": 2298,
  "input_bytes": 2298
}
```

## Run this target

```sh
python3 parsarium.py build mp3 c libmad
python3 parsarium.py run mp3 c libmad controls/mp3/tone-44k-mono.mp3
```
