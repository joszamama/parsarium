# openpnp-opencv — PNG / Java

- **Pinned release:** `4.9.0-0`
- **Upstream:** [source repository](<https://github.com/openpnp/opencv>) · [Maven Central](<https://central.sonatype.com/artifact/org.openpnp/opencv>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/openpnp_opencv/README.md)

```sh
python3 parsarium.py build png java openpnp_opencv
python3 parsarium.py run png java openpnp_opencv controls/png/red-green.png
```
