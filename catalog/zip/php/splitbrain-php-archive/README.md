# splitbrain/php-archive — ZIP / PHP

- **Pinned release:** `1.5.1`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** splitbrain PHP ZIP reader
- **Local input API:** `splitbrain\PHPArchive\Zip::open(local path); contents; extract`
- **Documentation:** [API reference](<https://github.com/splitbrain/php-archive/blob/0d8801eaac5342b26ff1776089d4a124117b652c/README.md>)
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

Pure PHP ZIP reader with central-directory parsing and zlib decompression.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
