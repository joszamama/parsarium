# minizip-ng — ZIP / C

- **Pinned release:** `4.2.2`
- **License:** Zlib
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** MiniZip lineage
- **Local input API:** `mz_zip_reader_open_file; mz_zip_reader_entry_get_info; mz_zip_reader_entry_read`
- **Documentation:** [API reference](<https://github.com/zlib-ng/minizip-ng/blob/4.2.2/mz_zip_rw.h>)
- **Catalog evidence:** [parser record](../../../../data/c/zip/parsers.json) · [control verification](../../../../data/c/zip/verification.json) · [within-ecosystem ranking](../../../../data/c/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

Separate maintained package descended from classic MiniZip; not an independent family claim.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
