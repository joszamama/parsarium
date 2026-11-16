# pymp4 — MP4 / Python

- **Pinned release:** `1.4.0`
- **License:** Apache-2.0
- **Parsed scope:** ftyp and moov boxes
- **Underlying family:** pymp4 Construct box parser
- **Local input API:** `pymp4.parser.Box.parse_stream(local byte stream)`
- **Documentation:** [API reference](<https://pypi.org/project/pymp4/1.4.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "first_box": "ftyp",
  "major_brand": "isom",
  "second_box": "moov"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/pymp4/README.md)

```sh
python3 parsarium.py build mp4 python pymp4
python3 parsarium.py run mp4 python pymp4 controls/mp4/red-av.mp4
```
