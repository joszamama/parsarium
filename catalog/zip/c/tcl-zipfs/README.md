# tcl-zipfs — ZIP / C

- **Pinned release:** `9.1.0`
- **License:** TCL
- **Parsed scope:** mounted ZIP entry name and decompressed entry bytes
- **Underlying family:** Tcl Zipfs ZIP reader
- **Local input API:** `TclZipfs_Mount(interp, local_zip_path, mountpoint, NULL); Tcl_OpenFileChannel and Tcl_Read`
- **Documentation:** [API reference](<https://www.tcl-lang.org/man/tcl9.1/TclLib/zipfs.html>)
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

Tcl core Zipfs parses ZIP records and uses zlib for DEFLATE. The C API is third-party to ISO C, despite being bundled with the Tcl runtime.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
