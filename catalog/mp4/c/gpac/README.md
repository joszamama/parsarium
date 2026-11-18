# gpac — MP4 / C

- **Pinned release:** `26.07.0`
- **Upstream:** [source repository](<https://github.com/gpac/gpac>)
- **License:** LGPL-2.1-or-later
- **Parsed scope:** two ISO media tracks, 2x2 video dimensions and duration
- **Underlying family:** GPAC native ISO media parser
- **Local input API:** `gf_isom_open(local filename, GF_ISOM_OPEN_READ); gf_isom_get_track_count/media_type/visual_info/duration`
- **Documentation:** [API reference](<https://doxygen.gpac.io/group__isogen__grp.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "video_tracks": 1,
  "audio_tracks": 1,
  "width": 2,
  "height": 2,
  "duration_ms": 1000
}
```

C and C++ call sites share the same gpac native MP4 parser. GPAC MP4Box is a CLI alias within the gpac package, not another package row.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/c/gpac/README.md)

```sh
python3 parsarium.py build mp4 c gpac
python3 parsarium.py run mp4 c gpac controls/mp4/red-av.mp4
```
