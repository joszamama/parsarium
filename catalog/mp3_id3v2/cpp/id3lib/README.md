# id3lib — MP3 with ID3v2 / C++

- **Pinned release:** `3.8.3`
- **License:** LGPL-2.0-or-later
- **Parsed scope:** ID3v2 title and frame count in a valid tagged MP3
- **Underlying family:** id3lib ID3v2 parser
- **Local input API:** `ID3_Tag::Link(local filename, ID3TT_ID3V2); Find(ID3FID_TITLE); GetField(ID3FN_TEXT)->Get`
- **Documentation:** [API reference](<https://id3lib.sourceforge.net/api/index.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "frames": 4
}
```

The C API wraps the same C++ id3lib engine used by the native C++ adapter. Both are one package path per ecosystem, not independent tag parsers.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
