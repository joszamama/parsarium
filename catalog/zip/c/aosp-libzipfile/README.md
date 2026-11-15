# aosp-libzipfile — ZIP / C

- **Pinned release:** `android-4.4.4_r2`
- **License:** Apache-2.0
- **Parsed scope:** entry name and decompressed entry bytes from local ZIP bytes
- **Underlying family:** AOSP libzipfile ZIP reader
- **Local input API:** `init_zipfile(const void* data, size_t size); iterate_zipfile; get_zipentry_name; decompress_zipentry`
- **Documentation:** [API reference](<https://android.googlesource.com/platform/system/core/+/refs/tags/android-4.4.4_r2/include/zipfile/zipfile.h>)
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

Standalone source build of the Android Open Source Project libzipfile C module; own central-directory parser, using zlib for DEFLATE. It is used here as a third-party package outside the Android runtime.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
