# miniz — ZIP / C++

- **Pinned release:** `3.1.2`
- **Upstream:** [source repository](<https://github.com/richgel999/miniz>)
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** miniz ZIP reader
- **Local input API:** `mz_zip_reader_init_file; mz_zip_reader_file_stat; mz_zip_reader_extract_to_heap`
- **Documentation:** [API reference](<https://github.com/richgel999/miniz/blob/3.1.2/miniz_zip.h>)
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

miniz archive reader; its DEFLATE implementation is integrated. The C++ path reuses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/miniz/README.md)

```sh
python3 parsarium.py build zip cpp miniz
python3 parsarium.py run zip cpp miniz controls/zip/hello.zip
```
