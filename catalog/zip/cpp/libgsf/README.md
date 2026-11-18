# libgsf — ZIP / C++

- **Pinned release:** `1.14.60`
- **Upstream:** [source repository](<https://gitlab.gnome.org/GNOME/libgsf>) · [Debian](<https://tracker.debian.org/pkg/libgsf>)
- **License:** LGPL-2.1-only
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** libgsf ZIP reader
- **Local input API:** `gsf_input_stdio_new; gsf_infile_zip_new; gsf_infile_child_by_index; gsf_input_read`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/libgsf/api/gsf-Zip.html>)
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

Own ZIP directory and entry API; uses compression dependencies for DEFLATE. The C++ path reuses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/cpp/libgsf/README.md)

```sh
python3 parsarium.py build zip cpp libgsf
python3 parsarium.py run zip cpp libgsf controls/zip/hello.zip
```
