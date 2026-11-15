# mp4v2 — MP4 / C++

- **Pinned release:** `2.1.3`
- **License:** MPL-1.1
- **Parsed scope:** two MP4 tracks and 2x2 video dimensions
- **Underlying family:** MP4v2 native MP4 atom parser
- **Local input API:** `MP4Read(local filename); MP4GetNumberOfTracks; MP4FindTrackId; MP4GetTrackVideoWidth/Height`
- **Documentation:** [API reference](<https://github.com/enzo1982/mp4v2/blob/v2.1.3/include/mp4v2/file.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2,
  "video_tracks": 1,
  "audio_tracks": 1,
  "width": 2,
  "height": 2
}
```

C and C++ call sites share MP4v2 native parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
