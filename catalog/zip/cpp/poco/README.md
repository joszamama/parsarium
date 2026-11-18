# poco — ZIP / C++

- **Pinned release:** `1.15.4`
- **Upstream:** [source repository](<https://github.com/pocoproject/poco>) · [Debian](<https://tracker.debian.org/pkg/poco>)
- **License:** BSL-1.0
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** POCO Zip reader
- **Local input API:** `Poco::Zip::ZipArchive(std::istream&); headerBegin; Poco::Zip::ZipInputStream(std::istream&, ZipLocalFileHeader)`
- **Documentation:** [API reference](<https://github.com/pocoproject/poco/blob/poco-1.15.4-release/Zip/include/Poco/Zip/ZipArchive.h>)
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

POCO parses ZIP archive headers in its Zip library and decompresses entries with its bundled zlib; independent package API from the C-cell libraries.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/poco/README.md)

```sh
python3 parsarium.py build zip cpp poco
python3 parsarium.py run zip cpp poco controls/zip/hello.zip
```
