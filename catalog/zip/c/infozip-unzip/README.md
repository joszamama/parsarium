# infozip-unzip — ZIP / C

- **Pinned release:** `6.0`
- **License:** Info-ZIP
- **Parsed scope:** entry name parsed by Info-ZIP listing and decompressed entry bytes from its C API
- **Underlying family:** Info-ZIP UnZip 6.0 engine
- **Local input API:** `UzpAltMain on a local ZIP path with listing callback; UzpUnzipToMemory(local ZIP path, parsed entry name); UzpFreeMemBuffer`
- **Documentation:** [API reference](<https://github.com/madler/unzip/blob/master/unzip.h>)
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

Official Info-ZIP UnZip 6.0 source exposes a C DLL API. This path compiles its library objects and calls the API directly; it is separate from MiniZip, unzipLIB, and other ZIP engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
