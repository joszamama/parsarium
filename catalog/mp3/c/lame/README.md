# lame — MP3 / C

- **Pinned release:** `4.0`
- **Upstream:** [source repository](<https://github.com/lameproject/lame>) · [Debian](<https://tracker.debian.org/pkg/lame>)
- **License:** LGPL-2.0-or-later
- **Parsed scope:** MP3 frame header and 576 decoded PCM samples from ID3v2-tagged local bytes; tag text is not exposed
- **Underlying family:** LAME HIP decoder interface over libmpg123
- **Local input API:** `hip_decode_init; hip_decode1_headers(local tagged MP3 bytes); inspect mp3data_struct; hip_decode_exit`
- **Documentation:** [API reference](<https://github.com/lameproject/lame/blob/master/include/lame.h>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control verification](../../../../data/c/mp3/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bitrate_kbps": 32,
  "decoded_samples": 576
}
```

The pinned LAME HIP interface accepts the full tagged control and returns MP3 frame fields; the installed libmp3lame links the separately verified libmpg123 decoder. C and C++ use one C library.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/c/lame/README.md)

```sh
python3 parsarium.py build mp3 c lame
python3 parsarium.py run mp3 c lame controls/mp3/id3v2-tagged-tone.mp3
```
