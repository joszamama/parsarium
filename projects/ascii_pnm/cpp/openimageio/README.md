# OpenImageIO — ASCII PNM / C++

Pinned OpenImageIO release: `3.2.2.0` from the official source archive. The [ImageInput API](https://openimageio.readthedocs.io/en/v3.2.2.0/imageinput.html) opens a local PNM file, reads the image specification, and decodes pixels. The harness writes supplied bytes to a temporary `.ppm` file and accepts ASCII PNM images with one or three channels. The observed result records dimensions, the `pnm` reader identity, the ASCII flag, and the first two RGB samples (grayscale samples are repeated across RGB). For a one-pixel image, `second` is `null`.

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp openimageio
python3 parsarium.py run ascii_pnm cpp openimageio controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp openimageio CORPUS_DIR runs/pnm-openimageio-replay
python3 parsarium.py afl build ascii_pnm cpp openimageio
python3 parsarium.py afl prepare ascii_pnm cpp openimageio runs/pnm-openimageio-afl
```

Replace `CORPUS_DIR` with a directory of PNM inputs. AFL++ preparation seeds a run but does not start a campaign. See the [manifest](manifest.json), [control receipt](verification.json), and [catalog record](../../../../catalog/ascii_pnm/cpp/openimageio/README.md).

The pinned source build embeds OpenImageIO's own PNM plugin. The valid P3 control covers 150 lines in `src/pnm.imageio/pnminput.cpp`; the [AFL++ receipt](../../../../fuzzing/afl-native/ascii_pnm/cpp/openimageio/verification.json) records 1,507 edges. A separate [fixed-input feedback check](../../../../fuzzing/afl-native/ascii_pnm/cpp/openimageio/feedback-validation.json) confirms an identical map on repeat and a different map for a valid P2 grayscale image. These checks run no mutation campaign.
