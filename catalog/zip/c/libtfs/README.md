# libtfs — ZIP / C

- **Pinned release:** `v0.13.0`
- **License:** BSD-2-Clause
- **Parsed scope:** mounted ZIP entry name and decompressed entry bytes
- **Underlying family:** libtfs C facade over libzip ZIP backend
- **Local input API:** `tebako_fs_init_from_file(const char* archive_path, const char* mount_point); tebako_fs_opendir/readdir; tebako_fs_open/read`
- **Documentation:** [API reference](<https://github.com/tamatebako/libtfs/blob/v0.13.0/include/tebako/fs/c_api.h>)
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

The documented C facade uses a C++ ZIP backend linked against libzip. This is a distinct package path but shares the libzip parser engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
