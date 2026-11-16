# gopkg.in/gographics/imagick.v3/imagick — PNG / Go

Pinned release: `v3.7.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/gopkg-in-gographics-imagick-v3-imagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py run png go gopkg_in_gographics_imagick_v3_imagick controls/png/red-green.png
python3 parsarium.py replay png go gopkg_in_gographics_imagick_v3_imagick CORPUS_DIR runs/png-gopkg_in_gographics_imagick_v3_imagick-replay
python3 parsarium.py afl build png go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py afl prepare png go gopkg_in_gographics_imagick_v3_imagick runs/png-gopkg_in_gographics_imagick_v3_imagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
