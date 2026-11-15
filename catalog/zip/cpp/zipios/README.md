# zipios — ZIP / C++

- **Pinned release:** `2.3.4`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Zipios ZIP reader
- **Local input API:** `zipios::ZipFile(const std::string&); entries; getInputStream(const std::string&)`
- **Documentation:** [API reference](<https://github.com/Zipios/Zipios/blob/2.3.4/zipios/zipfile.hpp>)
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

Zipios parses ZIP archives with its own C++ reader and uses zlib for decompression.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
