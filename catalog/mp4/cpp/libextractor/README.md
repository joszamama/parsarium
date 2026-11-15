# libextractor — MP4 / C++

- **Pinned release:** `1.20`
- **License:** GPL-3.0-or-later
- **Parsed scope:** QT/MP4 plugin parsed MIME type, title, duration and 2x2 video dimensions
- **Underlying family:** GNU libextractor native QT/MP4 metadata parser
- **Local input API:** `EXTRACTOR_plugin_add("qt"); EXTRACTOR_extract(local MP4 filename, callback) returns format-specific metadata`
- **Documentation:** [API reference](<https://www.gnu.org/software/libextractor/manual/extractor.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "duration_seconds": 1,
  "width": 2,
  "height": 2
}
```

C and C++ adapters call the same libextractor qt plugin; its exact installed native plugin hash is pinned.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
