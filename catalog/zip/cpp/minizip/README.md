# minizip — ZIP / C++

- **Pinned release:** `1.4`
- **License:** Zlib
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** classic MiniZip
- **Local input API:** `unzOpen64(const char*); unzGetGlobalInfo64; unzGetCurrentFileInfo64; unzReadCurrentFile`
- **Documentation:** [API reference](<https://github.com/madler/zlib/blob/v1.4/contrib/minizip/unzip.h>)
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

Classic MiniZip from the zlib contrib/minizip source subtree; separate from minizip-ng but related lineage. The C++ path reuses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
