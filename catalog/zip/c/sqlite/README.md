# sqlite — ZIP / C

- **Pinned release:** `3.54.1`
- **License:** Public-Domain
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** SQLite Zipfile virtual table with zlib DEFLATE
- **Local input API:** `sqlite3_zipfile_init(db,0,0); sqlite3_prepare_v2 SELECT name,data FROM zipfile(?1); bind local ZIP path; sqlite3_step`
- **Documentation:** [API reference](<https://www.sqlite.org/zipfile.html>)
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

Official SQLite ext/misc/zipfile.c extension parses ZIP archive records and delegates DEFLATE to zlib; its repository stars measure all SQLite usage, not Zipfile adoption.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
