# dr_libs — MP3 with ID3v2 / C++

- **Pinned release:** `mp3-0.7.4`
- **License:** Unlicense OR MIT-0
- **Parsed scope:** Tagged MP3 audio decode and raw ID3v2 tag recognition; does not decode ID3v2 text frames
- **Underlying family:** dr_mp3 over minimp3
- **Local input API:** `drmp3_init_file_with_metadata(local filename, callback); drmp3_read_pcm_frames_s16`
- **Documentation:** [API reference](<https://github.com/mackron/dr_libs/blob/mp3-0.7.4/dr_mp3.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "decoded_frames": 1,
  "id3v2_bytes": 101
}
```

Standalone dr_libs release is a separate package path from miniaudio, but miniaudio embeds dr_mp3 and both derive MP3 decoding from minimp3. C and C++ adapters share this header.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
