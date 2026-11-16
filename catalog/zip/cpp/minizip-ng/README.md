# minizip-ng — ZIP / C++

- **Pinned release:** `4.2.2`
- **License:** Zlib
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** MiniZip lineage
- **Local input API:** `mz_zip_reader_open_file; mz_zip_reader_entry_get_info; mz_zip_reader_entry_read`
- **Documentation:** [API reference](<https://github.com/zlib-ng/minizip-ng/blob/4.2.2/mz_zip_rw.h>)
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

Separate maintained package descended from classic MiniZip; not an independent family claim. The C++ path reuses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/minizip-ng/README.md)

```sh
python3 parsarium.py build zip cpp minizip-ng
python3 parsarium.py run zip cpp minizip-ng controls/zip/hello.zip
```
