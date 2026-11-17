# mpg123 — MP3 / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.33.7`
- **License:** LGPL-2.1-only
- **Parser family:** libmpg123 MPEG audio decoder
- **Local input API:** `mpg123_open_feed(mh); mpg123_feed(mh, local bytes, size); mpg123_decode_frame() until MPG123_NEED_MORE; mpg123_getformat(); mpg123_info2()`
- **Documentation:** [API reference](<https://www.mpg123.de/api/group__mpg123__input.shtml>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control result](../../../../projects/mp3/c/mpg123/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "layer": 3,
  "frames": 11,
  "decoded_samples": 12672
}
```

## Run this target

```sh
python3 parsarium.py build mp3 c mpg123
python3 parsarium.py run mp3 c mpg123 controls/mp3/tone-44k-mono.mp3
```
