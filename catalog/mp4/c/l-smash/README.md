# l-smash — MP4 / C

- **Pinned release:** `2.14.5`
- **License:** ISC
- **Parsed scope:** two MP4 tracks, one video and one audio, 2x2 video display dimensions and 1000 ms movie duration
- **Underlying family:** L-SMASH native ISO BMFF/MP4 box parser
- **Local input API:** `lsmash_open_file(local path, input mode 1); lsmash_set_file; lsmash_read_file; lsmash_get_movie_parameters, lsmash_get_media_parameters and lsmash_get_track_parameters`
- **Documentation:** [API reference](<https://github.com/l-smash/l-smash/blob/v2.14.5/lsmash.h>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "video": 1,
  "audio": 1,
  "width": 2,
  "height": 2,
  "duration_ms": 1000
}
```

Separate C library parser; no other accepted C MP4 package in this cell uses L-SMASH.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
