# vlc — MP3 / C++

- **Pinned release:** `3.0.24`
- **Upstream:** [source repository](<https://code.videolan.org/videolan/vlc>) · [Debian](<https://tracker.debian.org/pkg/vlc>)
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** ID3v2 title and recognized MP3 audio track from valid local tagged MP3
- **Underlying family:** VLC media parser with bundled TagLib and MPEG audio plugins
- **Local input API:** `libvlc_media_new_path(instance, local filename); libvlc_media_parse_with_options; libvlc_media_get_meta; libvlc_media_tracks_get`
- **Documentation:** [API reference](<https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3/parsers.json) · [control verification](../../../../data/cpp/mp3/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "audio_tracks": 1,
  "mp3_tracks": 1
}
```

The verified Docker routes statically register filesystem, skiptags, es, packetizer_mpegaudio and taglib. Both VLC native ID3v2 code and VLC-pinned, patched TagLib 1.13.1 parse the valid tag. C and C++ call sites share this underlying parser family; the separate TagLib package paths use TagLib 2.3.2.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/cpp/vlc/README.md)

```sh
python3 parsarium.py build mp3 cpp vlc
python3 parsarium.py run mp3 cpp vlc controls/mp3/id3v2-tagged-tone.mp3
```
