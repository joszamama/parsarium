# zziplib — ZIP / C

- **Pinned release:** `0.13.80`
- **License:** GPL-2.0-or-later
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** ZZIPlib ZIP reader
- **Local input API:** `zzip_dir_open; zzip_readdir; zzip_file_open; zzip_file_read`
- **Documentation:** [API reference](<https://github.com/gdraheim/zziplib/blob/v0.13.80/zzip/zzip.h>)
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

Own ZIP archive reader; uses zlib for DEFLATE.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/c/zziplib/README.md)

```sh
python3 parsarium.py build zip c zziplib
python3 parsarium.py run zip c zziplib controls/zip/hello.zip
```
