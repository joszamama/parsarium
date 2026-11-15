# troldal-zippy — ZIP / C++

- **Pinned release:** `cci.20200622`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Troldal Zippy wrapper over bundled miniz
- **Local input API:** `Zippy::ZipArchive::Open(const std::string&); GetEntryNames; GetEntry; ZipEntry::GetDataAsString`
- **Documentation:** [API reference](<https://github.com/troldal/KZip/blob/a838de8522f9051df0d1b202473bb6befe648702/library/Zippy/ZipArchive.hpp>)
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

Distinct C++ package API with bundled miniz; shares underlying parser lineage with miniz and kuba-zip.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
