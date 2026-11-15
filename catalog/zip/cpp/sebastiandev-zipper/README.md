# sebastiandev-zipper — ZIP / C++

- **Pinned release:** `1.0.3`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Sebastian Zipper wrapper over classic MiniZip fork
- **Local input API:** `zipper::Unzipper(local filename); entries(); extractEntryToMemory(entry name, vector)`
- **Documentation:** [API reference](<https://github.com/sebastiandev/zipper/blob/v1.0.3/README.md>)
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

Distinct tagged C++ package API from Lecrapouille/zipper, despite the shared name. Both use classic MiniZip lineage; this package pins its own Lecrapouille/minizip submodule at commit 7619140. Tag v1.0.3 contains VERSION.txt 1.0.2, recorded in source lock.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
