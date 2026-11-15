# openpnp-opencv — PNG / Java

- **Pinned release:** `4.9.0-0`
- **License:** BSD-3-Clause
- **Parsed scope:** PNG dimensions
- **Underlying family:** OpenPnP Java JNI packaging of native OpenCV image decoder
- **Local input API:** `OpenCV.loadLocally(); Imgcodecs.imread(path,IMREAD_UNCHANGED)`
- **Documentation:** [API reference](<https://github.com/openpnp/opencv>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
