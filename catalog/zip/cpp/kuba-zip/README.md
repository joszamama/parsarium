# kuba-zip — ZIP / C++

- **Pinned release:** `0.3.2`
- **License:** Unlicense
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** kuba-zip wrapper over bundled miniz
- **Local input API:** `zip_open(const char*, int, char); zip_entries_total; zip_entry_openbyindex; zip_entry_name; zip_entry_read`
- **Documentation:** [API reference](<https://github.com/kuba--/zip/blob/v0.3.2/src/zip.h>)
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

Distinct package API that embeds miniz for ZIP parsing and DEFLATE; shares underlying parser lineage with miniz. The C++ path reuses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
