# libc7zip — ZIP / C++

- **Pinned release:** `v1.10.0`
- **License:** MIT AND MPL-2.0 AND LGPL-2.1-or-later
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libc7zip → lib7zip → 7-Zip ZIP engine
- **Local input API:** `in_stream_new with local FILE read/seek callbacks; archive_open; archive_get_item_count; item_get_string_property(kpidPath); archive_extract_item to output callback`
- **Documentation:** [API reference](<https://github.com/itchio/libc7zip/blob/v1.10.0/include/libc7zip.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/zip/parsers.json) · [control verification](../../../../data/cpp/zip/verification.json) · [within-ecosystem ranking](../../../../data/cpp/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

Tagged MIT C facade vendors an MPL-2.0 lib7zip fork and loads a 7-Zip 26.03 engine; a distinct package path sharing the 7-Zip parser family with bit7z in C++. The C++17 call site links the same SHA-pinned C facade and 7-Zip engine as the C cell.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
