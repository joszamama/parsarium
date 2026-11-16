# libgsf — ZIP / C

- **Pinned release:** `1.14.60`
- **License:** LGPL-2.1-only
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libgsf ZIP reader
- **Local input API:** `gsf_input_stdio_new; gsf_infile_zip_new; gsf_infile_child_by_index; gsf_input_read`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/libgsf/api/gsf-Zip.html>)
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

Own ZIP directory and entry API; uses compression dependencies for DEFLATE.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/c/libgsf/README.md)

```sh
python3 parsarium.py build zip c libgsf
python3 parsarium.py run zip c libgsf controls/zip/hello.zip
```
