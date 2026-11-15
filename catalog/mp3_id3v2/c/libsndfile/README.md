# libsndfile — MP3 with ID3v2 / C

- **Pinned release:** `1.2.2`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** ID3v2 title, MPEG Layer III sample rate/channels/frame count, and one decoded audio frame
- **Underlying family:** libsndfile MPEG frontend over libmpg123 decoder and ID3v2 reader
- **Local input API:** `sf_open(local tagged MP3 filename, SFM_READ, SF_INFO); sf_get_string(SF_STR_TITLE); sf_readf_float decoded audio frame`
- **Documentation:** [API reference](<https://libsndfile.github.io/libsndfile/api.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "sample_rate": 8000,
  "channels": 1,
  "frames": 8000,
  "decoded_frames": 1
}
```

The pinned libsndfile mpeg_decode.c uses mpg123_id3 and mpg123 audio decoding. This is a distinct package input API sharing the separately counted libmpg123 syntax engine. C and C++ call sites use the same C implementation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
