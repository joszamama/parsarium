# physfs — ZIP / C

- **Pinned release:** `3.2.0`
- **License:** Zlib
- **Parsed scope:** mounted ZIP entry name and decompressed entry bytes
- **Underlying family:** PhysicsFS ZIP archiver
- **Local input API:** `PHYSFS_mount(local ZIP path); PHYSFS_enumerateFiles; PHYSFS_openRead; PHYSFS_readBytes`
- **Documentation:** [API reference](<https://github.com/icculus/physfs/blob/release-3.2.0/src/physfs.h>)
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

PhysicsFS provides a distinct virtual filesystem package API with an internal ZIP archive handler; its C++ call site reuses this C library.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
