# metaprobe — MP4 / JavaScript

- **Pinned release:** `0.2.1`
- **License:** MIT
- **Parsed scope:** video_metadata
- **Underlying family:** metaprobe Rust core
- **Local input API:** `extractMeta(path,{hash:false})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/metaprobe>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "kind": "video",
  "format": "mp4",
  "width": 2,
  "height": 2,
  "title": "Parsarium",
  "duration": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/metaprobe/README.md)

```sh
python3 parsarium.py build mp4 javascript metaprobe
python3 parsarium.py run mp4 javascript metaprobe controls/mp4/red-av.mp4
```
