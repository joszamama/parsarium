# bit7z — ZIP / C++

- **Pinned release:** `4.1.0`
- **License:** MPL-2.0
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** bit7z wrapper over SevenZip ZIP reader
- **Local input API:** `bit7z::BitArchiveReader(Bit7zLibrary, local path, BitFormat::Zip); itemsCount; itemAt; extractTo(buffer, index)`
- **Documentation:** [API reference](<https://github.com/rikyoz/bit7z/blob/v4.1.0/include/bit7z/bitarchivereader.hpp>)
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

Distinct C++ wrapper API; ZIP parsing and decompression use an exact-release, binary-hashed SevenZip 26.04 shared library. Not an independent decoder from SevenZip.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
