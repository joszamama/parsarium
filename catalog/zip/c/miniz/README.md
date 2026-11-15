# miniz — ZIP / C

- **Pinned release:** `3.1.2`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** miniz ZIP reader
- **Local input API:** `mz_zip_reader_init_file; mz_zip_reader_file_stat; mz_zip_reader_extract_to_heap`
- **Documentation:** [API reference](<https://github.com/richgel999/miniz/blob/3.1.2/miniz_zip.h>)
- **Catalog evidence:** [parser record](../../../../data/c/zip/parsers.json) · [control verification](../../../../data/c/zip/verification.json) · [within-ecosystem ranking](../../../../data/c/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

miniz archive reader; its DEFLATE implementation is integrated.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
