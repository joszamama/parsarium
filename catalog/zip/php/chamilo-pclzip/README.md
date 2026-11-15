# chamilo/pclzip — ZIP / PHP

- **Pinned release:** `v2.8.5`
- **License:** LGPL-2.1
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Chamilo PclZip fork
- **Local input API:** `PclZip(local path); extract(PCLZIP_OPT_EXTRACT_AS_STRING)`
- **Documentation:** [API reference](<https://github.com/chamilo/pclzip/blob/af10d07a39922b0789bf761524a22ecefc01d405/readme.txt>)
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

A separately released Composer package of the PclZip PHP reader; same underlying parser lineage as pclzip/pclzip.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
