# karchive — ZIP / C++

- **Pinned release:** `6.31.0`
- **License:** BSD-2-Clause AND LGPL-2.0-only AND LGPL-2.0-or-later AND (LGPL-2.0-only OR LGPL-3.0-only)
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** KArchive KZip reader
- **Local input API:** `KZip(local filename); open(QIODevice::ReadOnly); directory()->entries; KArchiveDirectory::file; KArchiveFile::data`
- **Documentation:** [API reference](<https://api.kde.org/kzip.html>)
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

KDE Frameworks KArchive exposes its own ZIP reader through KZip and Qt; the same package is counted only once.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/karchive/README.md)

```sh
python3 parsarium.py build zip cpp karchive
python3 parsarium.py run zip cpp karchive controls/zip/hello.zip
```
