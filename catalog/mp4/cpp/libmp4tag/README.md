# libmp4tag — MP4 / C++

- **Pinned release:** `2.0.4`
- **License:** Zlib
- **Parsed scope:** MP4 title metadata and 1128 ms duration
- **Underlying family:** libmp4tag native MP4 atom and tag parser
- **Local input API:** `mp4tag_open(local MP4 filename); mp4tag_parse; mp4tag_get_tag_by_name; mp4tag_duration`
- **Documentation:** [API reference](<https://libmp4tag.sourceforge.io/ (GettingTags and Initializing in pinned release wiki)>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "duration_ms": 1128
}
```

C and C++ adapters call the same published C API and native parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
