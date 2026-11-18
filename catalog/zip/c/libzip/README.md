# libzip — ZIP / C

- **Pinned release:** `1.12.1`
- **Upstream:** [source repository](<https://github.com/nih-at/libzip>) · [Debian](<https://tracker.debian.org/pkg/libzip>)
- **License:** BSD-3-Clause
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libzip ZIP reader
- **Local input API:** `zip_open(const char*); zip_get_num_entries; zip_stat_index; zip_fopen_index and zip_fread`
- **Documentation:** [API reference](<https://libzip.org/documentation/zip_open/>)
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

Own ZIP archive reader and entry API.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/c/libzip/README.md)

```sh
python3 parsarium.py build zip c libzip
python3 parsarium.py run zip c libzip controls/zip/hello.zip
```
