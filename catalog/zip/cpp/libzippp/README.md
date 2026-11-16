# libzippp — ZIP / C++

- **Pinned release:** `7.1-1.10.1`
- **License:** BSD-3-Clause
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libzippp wrapper over libzip
- **Local input API:** `libzippp::ZipArchive(const std::string&); open(ReadOnly); getEntries; ZipEntry::readAsText`
- **Documentation:** [API reference](<https://github.com/ctabin/libzippp/blob/libzippp-v7.1-1.10.1/src/libzippp.h>)
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

Distinct C++ package API built from pinned source; shares the libzip ZIP reader and installed libzip 1.12.1 with the libzip path.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/libzippp/README.md)

```sh
python3 parsarium.py build zip cpp libzippp
python3 parsarium.py run zip cpp libzippp controls/zip/hello.zip
```
