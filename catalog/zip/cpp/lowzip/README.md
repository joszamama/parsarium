# lowzip — ZIP / C++

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** lowzip ZIP reader
- **Local input API:** `lowzip_init_archive with read_callback over local ZIP bytes; lowzip_locate_file; lowzip_get_data`
- **Documentation:** [API reference](<https://github.com/svaarala/lowzip/blob/v1.0.1/README.md>)
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

Independent footprint-optimized ZIP reader with built-in DEFLATE; the C++ path compiles the same source and C API. The C++ path reuses the exact C-cell source release and parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
