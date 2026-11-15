# physfs — ZIP / C++

- **Pinned release:** `3.2.0`
- **License:** Zlib
- **Parsed scope:** mounted ZIP entry name and decompressed entry bytes
- **Underlying family:** PhysicsFS ZIP archiver
- **Local input API:** `PHYSFS_mount(local ZIP path); PHYSFS_enumerateFiles; PHYSFS_openRead; PHYSFS_readBytes`
- **Documentation:** [API reference](<https://github.com/icculus/physfs/blob/release-3.2.0/src/physfs.h>)
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

Same PhysicsFS release and ZIP handler as the C cell; the C API is compiled and invoked from a C++17 translation unit.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
