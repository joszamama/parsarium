# libheif — MP4 / C

- **Pinned release:** `1.23.7`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** MP4 video sequence track and 2x2 image resolution; the library does not expose the audio track through this sequence API
- **Underlying family:** libheif native ISO BMFF image-sequence and MP4 parser
- **Local input API:** `heif_context_read_from_file(local MP4 path); heif_context_number_of_sequence_tracks; heif_context_get_track; heif_track_get_image_resolution`
- **Documentation:** [API reference](<https://github.com/strukturag/libheif/wiki/Reading-and-Writing-Sequences>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "sequence_tracks": 1,
  "video_tracks": 1,
  "width": 2,
  "height": 2
}
```

C and C++ adapters call the same libheif 1.23.7 C API and parser. This separate parser reads the MP4 video sequence and ignores audio.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
