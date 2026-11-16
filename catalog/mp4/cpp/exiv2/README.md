# exiv2 — MP4 / C++

- **Pinned release:** `0.28.9`
- **License:** GPL-2.0-or-later
- **Parsed scope:** MP4 major brand and video dimensions from parsed QuickTime XMP metadata
- **Underlying family:** Exiv2 native QuickTime/MP4 metadata parser
- **Local input API:** `Exiv2::ImageFactory::open(local MP4 filename); Image::readMetadata(); XmpData::findKey for QuickTime/MP4 fields`
- **Documentation:** [API reference](<https://exiv2.org/doc/classExiv2_1_1QuickTimeVideo.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "MP4 Base Media",
  "width": 2,
  "height": 2
}
```

Exiv2 has a native QuickTimeVideo reader in src/quicktimevideo.cpp; this is not the FFmpeg or TagLib parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/cpp/exiv2/README.md)

```sh
python3 parsarium.py build mp4 cpp exiv2
python3 parsarium.py run mp4 cpp exiv2 controls/mp4/red-av.mp4
```
