# tinytag — MP3 / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.3.2`
- **License:** MIT
- **Parser family:** TinyTag MPEG frame-header reader
- **Local input API:** `tinytag.TinyTag.get(file_obj=io.BytesIO(local bytes)) -> _MPEG reader`
- **Documentation:** [API reference](<https://github.com/tinytag/tinytag/blob/2.3.2/README.md#file-like-objects>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control result](../../../../projects/mp3/python/tinytag/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "bitrate_kbps": 64.0,
  "duration_us": 287347
}
```

## Run this target

```sh
python3 parsarium.py build mp3 python tinytag
python3 parsarium.py run mp3 python tinytag controls/mp3/tone-44k-mono.mp3
```
