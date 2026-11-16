# pytaglib — MP4 / Python

- **Pinned release:** `3.2.0`
- **License:** GPL-3.0-or-later
- **Parsed scope:** MP4 title metadata
- **Underlying family:** TagLib native MP4 parser
- **Local input API:** `taglib.File(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pytaglib/3.2.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/pytaglib/README.md)

```sh
python3 parsarium.py build mp4 python pytaglib
python3 parsarium.py run mp4 python pytaglib controls/mp4/red-av.mp4
```
