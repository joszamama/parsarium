# codem-isoboxer — MP4 / JavaScript

- **Pinned release:** `0.3.10`
- **Upstream:** [source repository](<https://github.com/Dash-Industry-Forum/codem-isoboxer>) · [npm](<https://www.npmjs.com/package/codem-isoboxer>)
- **License:** MIT
- **Parsed scope:** boxes+brand
- **Underlying family:** codem-isoboxer
- **Local input API:** `ISOBoxer.parseBuffer(ArrayBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/codem-isoboxer>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "boxes": [
    "ftyp",
    "moov",
    "free",
    "mdat"
  ],
  "brand": "isom"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/codem_isoboxer/README.md)

```sh
python3 parsarium.py build mp4 javascript codem_isoboxer
python3 parsarium.py run mp4 javascript codem_isoboxer controls/mp4/red-av.mp4
```
