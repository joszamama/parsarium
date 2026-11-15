# zipc — ZIP / C++

- **Pinned release:** `v1.3`
- **License:** BSD-2-Clause
- **Parsed scope:** decompressed bytes for a known named ZIP entry; no entry enumeration API verified
- **Underlying family:** zipc ZIP container reader with zlib DEFLATE
- **Local input API:** `zipcOpen(local_path,"r"); zipcOpenFile(archive,"hello.txt"); zipcFileRead; zipcFileFinish`
- **Documentation:** [API reference](<https://www.msweet.org/zipc/zipc.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/zip/parsers.json) · [control verification](../../../../data/cpp/zip/verification.json) · [within-ecosystem ranking](../../../../data/cpp/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "content": "parsarium\n"
}
```

zipc parses ZIP container records itself and uses zlib for DEFLATE. Its public reading API opens a named entry; this path does not claim enumeration or an observed entry count. The C++ path reuses the exact C-cell release and parser implementation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
