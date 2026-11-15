# zetacomponents/archive — ZIP / PHP

- **Pinned release:** `1.5.1`
- **License:** Apache-2.0
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Zeta Components custom PHP ZIP reader
- **Local input API:** `ezcArchive::open(local ZIP path, ZIP, readOnly options); iterate entries; extractCurrent`
- **Documentation:** [API reference](<https://zetacomponents.org/documentation/trunk/Archive/tutorial.html>)
- **Catalog evidence:** [parser record](../../../../data/php/zip/parsers.json) · [control verification](../../../../data/php/zip/verification.json) · [within-ecosystem ranking](../../../../data/php/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

Parses ZIP headers through its own PHP archive classes and uses zlib for DEFLATE; this adapter does not use ZipArchive.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
