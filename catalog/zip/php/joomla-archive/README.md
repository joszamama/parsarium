# joomla/archive — ZIP / PHP

- **Pinned release:** `4.0.0`
- **License:** GPL-2.0-or-later
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Joomla ZIP adapter over PHP ZipArchive
- **Local input API:** `Joomla\Archive\Archive::extract(local ZIP path, destination)`
- **Documentation:** [API reference](<https://github.com/joomla-framework/archive/blob/7a8d0eda637bd37bc3de744aa3e4ce516d4356b0/README.md>)
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

The installed PHP zip extension selects Joomla’s native ZipArchive branch; its source also has a custom ZIP reader fallback.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
