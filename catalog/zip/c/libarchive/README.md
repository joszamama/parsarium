# libarchive — ZIP / C

- **Pinned release:** `3.8.11`
- **License:** BSD-2-Clause
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libarchive ZIP reader
- **Local input API:** `archive_read_open_filename; archive_read_support_format_zip; archive_read_next_header and archive_read_data`
- **Documentation:** [API reference](<https://github.com/libarchive/libarchive/blob/v3.8.11/libarchive/archive.h>)
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

Own ZIP reader and entry data API; DEFLATE uses compression support.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/c/libarchive/README.md)

```sh
python3 parsarium.py build zip c libarchive
python3 parsarium.py run zip c libarchive controls/zip/hello.zip
```
