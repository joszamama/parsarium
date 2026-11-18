# node-video-lib — MP4 / JavaScript

- **Pinned release:** `2.5.0`
- **Upstream:** [source repository](<https://github.com/gkozlenko/node-video-lib>) · [npm](<https://www.npmjs.com/package/node-video-lib>)
- **License:** MIT
- **Parsed scope:** duration+tracks
- **Underlying family:** node-video-lib
- **Local input API:** `MovieParser.parse(fileDescriptor)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/node-video-lib>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "duration": 1,
  "tracks": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/node_video_lib/README.md)

```sh
python3 parsarium.py build mp4 javascript node_video_lib
python3 parsarium.py run mp4 javascript node_video_lib controls/mp4/red-av.mp4
```
