# jsmediatags — MP4 / JavaScript

- **Pinned release:** `3.9.7`
- **Upstream:** [source repository](<https://github.com/aadsm/jsmediatags>) · [npm](<https://www.npmjs.com/package/jsmediatags>)
- **License:** BSD-3-Clause
- **Parsed scope:** tags
- **Underlying family:** jsmediatags
- **Local input API:** `read(Uint8Array,{onSuccess,onError})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/jsmediatags>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "type": "MP4",
  "brand": "isom",
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/jsmediatags/README.md)

```sh
python3 parsarium.py build mp4 javascript jsmediatags
python3 parsarium.py run mp4 javascript jsmediatags controls/mp4/red-av.mp4
```
