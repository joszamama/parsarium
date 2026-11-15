# libmad — MP3 with ID3v2 / C

- **Pinned release:** `0.16.5`
- **License:** GPL-2.0-or-later
- **Parsed scope:** MPEG Layer III frame parsing and 576 PCM samples from an ID3v2-tagged local file; adapter skips tag header/body
- **Underlying family:** libmad MPEG audio decoder
- **Local input API:** `mad_stream_buffer(local bytes after ID3v2 tag); mad_stream_skip; mad_frame_decode; mad_synth_frame`
- **Documentation:** [API reference](<https://codeberg.org/tenacityteam/libmad/src/tag/0.16.5/include/mad.h.in>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
