# qarchive — ZIP / C++

- **Pinned release:** `2.2.8`
- **License:** BSD-3-Clause
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** QArchive wrapper over libarchive
- **Local input API:** `QArchive::MemoryExtractor(local path); finished output getFiles; fileInformation and MemoryFile::buffer`
- **Documentation:** [API reference](<https://github.com/antony-jr/QArchive/blob/v2.2.8/include/qarchivememoryextractor.hpp>)
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

Distinct Qt/C++ package API; ZIP parsing and decompression are provided by the pinned libarchive release.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
