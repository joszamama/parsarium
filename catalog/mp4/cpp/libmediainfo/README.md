# libmediainfo — MP4 / C++

- **Pinned release:** `26.10`
- **License:** BSD-2-Clause
- **Parsed scope:** MPEG-4 container, title, AVC video and AAC audio, 2x2 video dimensions
- **Underlying family:** MediaInfoLib native MPEG-4 parser
- **Local input API:** `MediaInfo::Open(local filename); MediaInfo::Get for container, tracks, title and dimensions`
- **Documentation:** [API reference](<https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "container": "MPEG-4",
  "title": "Parsarium",
  "video": "AVC",
  "audio": "AAC",
  "width": 2,
  "height": 2
}
```

C and native C++ call sites share MediaInfoLib MPEG-4 parser and ZenLib utility library.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/cpp/libmediainfo/README.md)

```sh
python3 parsarium.py build mp4 cpp libmediainfo
python3 parsarium.py run mp4 cpp libmediainfo controls/mp4/red-av.mp4
```
