# kiwilan/php-archive — ZIP / PHP

- **Pinned release:** `2.3.02`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Kiwilan archive wrapper over PHP ZipArchive
- **Local input API:** `Archive::read(local ZIP path); getFirst; getContents`
- **Documentation:** [API reference](<https://github.com/kiwilan/php-archive/blob/2e202603396a620720aad676c4037eebc0443090/README.md>)
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

Its ZIP reader delegates to PHP ZipArchive; the package also supports other archive formats.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
