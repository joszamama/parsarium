# mutagen — MP3 / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.48.1`
- **License:** GPL-2.0-or-later
- **Parser family:** Mutagen MP3/ID3 parser
- **Local input API:** `mutagen.mp3.MP3(io.BytesIO(local bytes)).info -> MPEGInfo`
- **Documentation:** [API reference](<https://mutagen.readthedocs.io/en/latest/api/mp3.html>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control result](../../../../projects/mp3/python/mutagen/verification.json)

## Observed control result

```json
{
  "version": 1,
  "layer": 3,
  "sample_rate": 44100,
  "channels": 1,
  "bitrate": 64000,
  "length_us": 287250
}
```

## Run this target

```sh
python3 parsarium.py build mp3 python mutagen
python3 parsarium.py run mp3 python mutagen controls/mp3/tone-44k-mono.mp3
```
