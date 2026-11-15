# zipper — ZIP / C++

- **Pinned release:** `4.0.0`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Zipper wrapper over classic MiniZip fork
- **Local input API:** `zipper::Unzipper(const std::string&); entries; extract(const std::string&, std::ostream&)`
- **Documentation:** [API reference](<https://github.com/Lecrapouille/zipper/blob/v4.0.0/include/Zipper/Unzipper.hpp>)
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

Distinct C++ package API; v4.0.0 includes a pinned MiniZip fork and zlib-ng submodule. Shares classic MiniZip lineage with minizip.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
