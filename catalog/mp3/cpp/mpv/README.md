# mpv — MP3 / C++

- **Pinned release:** `0.42.0`
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** ID3v2 title, MP3 audio track codec and duration from local tagged file
- **Underlying family:** libmpv local media frontend over FFmpeg libavformat and libavcodec
- **Local input API:** `mpv_create/initialize; mpv_command(loadfile, local filename); MPV_EVENT_FILE_LOADED; mpv_get_property metadata/by-key/title, track-list/0/codec, duration`
- **Documentation:** [API reference](<https://mpv.io/manual/stable/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3/parsers.json) · [control verification](../../../../data/cpp/mp3/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "codec": "mp3",
  "duration_ms": 1000
}
```

libmpv 0.42.0 calls FFmpeg 9.0.2 libavformat/id3v2.c and mp3dec.c, the same underlying parser family as the direct FFmpeg row and the C mpv row. The local-file catalog control reports the tag title, MP3 track codec, and duration. The AFL byte bridge uses mpv's fd://42 fuzz mode, disables decoding, and scopes feedback to those FFmpeg parsers and mpv's demux_lavf wrapper.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/cpp/mpv/README.md)

```sh
python3 parsarium.py build mp3 cpp mpv
python3 parsarium.py run mp3 cpp mpv controls/mp3_id3v2/tone-tags.mp3
```
