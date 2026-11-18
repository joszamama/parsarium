# unarr — ZIP / C

- **Pinned release:** `1.2.0`
- **Upstream:** [source repository](<https://github.com/selmf/unarr>) · [Debian](<https://tracker.debian.org/pkg/unarr>)
- **License:** LGPL-3.0-only
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** unarr ZIP reader
- **Local input API:** `ar_open_file(const char*); ar_open_zip_archive; ar_parse_entry; ar_entry_get_name; ar_entry_uncompress`
- **Documentation:** [API reference](<https://github.com/selmf/unarr/blob/v1.2.0/unarr.h.in>)
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

selmf/unarr fork of zeniko/unarr; its ZIP parser and decompression API are part of the pinned source package.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/c/unarr/README.md)

```sh
python3 parsarium.py build zip c unarr
python3 parsarium.py run zip c unarr controls/zip/hello.zip
```
