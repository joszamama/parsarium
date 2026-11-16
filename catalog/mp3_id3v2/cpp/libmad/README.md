# libmad — MP3 with ID3v2 / C++

- **Pinned release:** `0.16.5`
- **License:** GPL-2.0-or-later
- **Parsed scope:** MPEG Layer III frame parsing and 576 PCM samples from an ID3v2-tagged local file; adapter skips tag header/body
- **Underlying family:** libmad MPEG audio decoder
- **Local input API:** `mad_stream_buffer(local bytes after ID3v2 tag); mad_stream_skip; mad_frame_decode; mad_synth_frame`
- **Documentation:** [API reference](<https://codeberg.org/tenacityteam/libmad/src/tag/0.16.5/include/mad.h.in>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "layer": 3,
  "sample_rate": 8000,
  "bit_rate": 32000,
  "channels": 1,
  "decoded_samples": 576
}
```

libmad is the same decoder family linked by the separately counted SoX package. It parses MPEG audio frames, not ID3v2 text. The adapter skips the valid control tag using its syncsafe length before calling libmad.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/cpp/libmad/README.md)

```sh
python3 parsarium.py build mp3_id3v2 cpp libmad
python3 parsarium.py run mp3_id3v2 cpp libmad controls/mp3_id3v2/tone-tags.mp3
```
