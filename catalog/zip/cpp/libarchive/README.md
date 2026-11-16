# libarchive — ZIP / C++

- **Pinned release:** `3.8.11`
- **License:** BSD-2-Clause
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libarchive ZIP reader
- **Local input API:** `archive_read_open_filename; archive_read_support_format_zip; archive_read_next_header and archive_read_data`
- **Documentation:** [API reference](<https://github.com/libarchive/libarchive/blob/v3.8.11/libarchive/archive.h>)
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

Own ZIP reader and entry data API; DEFLATE uses compression support. The C++ path reuses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/libarchive/README.md)

```sh
python3 parsarium.py build zip cpp libarchive
python3 parsarium.py run zip cpp libarchive controls/zip/hello.zip
```
