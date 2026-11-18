# tinytag — MP4 / Python

- **Pinned release:** `2.3.2`
- **Upstream:** [source repository](<https://github.com/tinytag/tinytag>) · [PyPI](<https://pypi.org/project/tinytag/>)
- **License:** MIT
- **Parsed scope:** MP4 title and duration
- **Underlying family:** TinyTag MP4 parser
- **Local input API:** `tinytag.TinyTag.get(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/tinytag/2.3.2/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "duration_seconds": 1.0
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/tinytag/README.md)

```sh
python3 parsarium.py build mp4 python tinytag
python3 parsarium.py run mp4 python tinytag controls/mp4/red-av.mp4
```
