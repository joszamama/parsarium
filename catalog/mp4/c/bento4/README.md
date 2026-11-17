# bento4 — MP4 / C

- **Pinned release:** `1.6.0-641`
- **License:** GPL-2.0-or-later
- **Parsed scope:** MP4 major brand, two audio/video tracks and one-second duration
- **Underlying family:** Bento4 AP4 ISO BMFF core
- **Local input API:** `AP4_FileByteStream_Create(local filename, READ); AP4_File_FromStream; AP4_File_GetMovie/GetFileType; AP4_Movie_GetTrackCount/GetTrackByIndex/GetDurationMs`
- **Documentation:** [API reference](<https://github.com/axiomatic-systems/Bento4/blob/v1.6.0-641/Source/C%2B%2B/CApi/Bento4C.h>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom",
  "tracks": 2,
  "video_tracks": 1,
  "audio_tracks": 1,
  "duration_ms": 1000
}
```

C and C++ call sites share Bento4 AP4 core and C binding; C++ adapter compiles the C binding call site as C++.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/c/bento4/README.md)

```sh
python3 parsarium.py build mp4 c bento4
python3 parsarium.py run mp4 c bento4 controls/mp4/red-av.mp4
```
