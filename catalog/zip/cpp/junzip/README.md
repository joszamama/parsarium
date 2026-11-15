# junzip — ZIP / C++

- **Pinned release:** `v0.1.1`
- **License:** Unlicense
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** JUnzip ZIP record reader with zlib DEFLATE
- **Local input API:** `jzReadEndRecord(FILE*); jzReadCentralDirectory(FILE*, callback); jzReadLocalFileHeader; jzReadData`
- **Documentation:** [API reference](<https://github.com/jokkebk/JUnzip/blob/v0.1.1/junzip.h>)
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

JUnzip parses ZIP end, central and local records itself, then delegates DEFLATE decompression to zlib; separate package from Info-ZIP UnZip. The C++ path uses the exact C-cell release and parser implementation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
