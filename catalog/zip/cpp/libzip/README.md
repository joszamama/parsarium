# libzip — ZIP / C++

- **Pinned release:** `1.12.1`
- **License:** BSD-3-Clause
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libzip ZIP reader
- **Local input API:** `zip_open(const char*); zip_get_num_entries; zip_stat_index; zip_fopen_index and zip_fread`
- **Documentation:** [API reference](<https://libzip.org/documentation/zip_open/>)
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

Own ZIP archive reader and entry API. The C++ path reuses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/libzip/README.md)

```sh
python3 parsarium.py build zip cpp libzip
python3 parsarium.py run zip cpp libzip controls/zip/hello.zip
```
