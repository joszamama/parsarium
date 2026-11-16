# soluble/mediatools — MP4 / PHP

- **Pinned release:** `2.2.0`
- **License:** MIT
- **Parsed scope:** MP4 container, 2 × 2 H.264 video
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `VideoInfoReader::getInfo(local MP4 path); container, H.264 codec, and dimensions`
- **Documentation:** [API reference](<https://github.com/soluble-io/soluble-mediatools/blob/3c7b0cec78ee97f9a74443cb0eecf10504c1eec5/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "container": "mov,mp4,m4a,3gp,3g2,mj2",
  "video_codec": "h264",
  "width": 2,
  "height": 2
}
```

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/soluble_mediatools/README.md)

```sh
python3 parsarium.py build mp4 php soluble_mediatools
python3 parsarium.py run mp4 php soluble_mediatools controls/mp4/red-av.mp4
```
