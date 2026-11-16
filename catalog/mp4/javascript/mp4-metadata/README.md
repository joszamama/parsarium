# mp4-metadata — MP4 / JavaScript

- **Pinned release:** `1.0.2`
- **License:** MIT
- **Parsed scope:** creation_time
- **Underlying family:** mp4-metadata
- **Local input API:** `getCreationTime(Blob,{maxBytesRead})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp4-metadata>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "creationTime": "2020-01-02T03:04:05.000Z"
}
```

Browser FileReader requirement supplied by adapter using Blob.arrayBuffer in Node.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/mp4_metadata/README.md)

```sh
python3 parsarium.py build mp4 javascript mp4_metadata
python3 parsarium.py run mp4 javascript mp4_metadata controls/mp4/red-av.mp4
```
