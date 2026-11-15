# zziplib — ZIP / C++

- **Pinned release:** `0.13.80`
- **License:** GPL-2.0-or-later
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** ZZIPlib ZIP reader
- **Local input API:** `zzip_dir_open; zzip_readdir; zzip_file_open; zzip_file_read`
- **Documentation:** [API reference](<https://github.com/gdraheim/zziplib/blob/v0.13.80/zzip/zzip.h>)
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

Own ZIP archive reader; uses zlib for DEFLATE. The C++ path reuses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
