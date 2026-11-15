# mpv — MP3 with ID3v2 / C++

- **Pinned release:** `0.42.0`
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** ID3v2 title, MP3 audio track codec and duration from local tagged file
- **Underlying family:** libmpv local media frontend over FFmpeg libavformat and libavcodec
- **Local input API:** `mpv_create/initialize; mpv_command(loadfile, local filename); MPV_EVENT_FILE_LOADED; mpv_get_property metadata/by-key/title, track-list/0/codec, duration`
- **Documentation:** [API reference](<https://mpv.io/manual/stable/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "codec": "mp3",
  "duration_ms": 1000
}
```

libmpv links the same FFmpeg libraries used by the separately counted FFmpeg row; C and C++ use the same libmpv C API. The local loadfile command returns parsed metadata and MP3 track fields without playing sound.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
