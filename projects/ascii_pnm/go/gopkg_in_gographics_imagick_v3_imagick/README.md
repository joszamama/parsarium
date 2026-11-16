# gopkg.in/gographics/imagick.v3/imagick — ASCII PNM / Go

Pinned release: `v3.7.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/gopkg-in-gographics-imagick-v3-imagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py run ascii_pnm go gopkg_in_gographics_imagick_v3_imagick controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go gopkg_in_gographics_imagick_v3_imagick CORPUS_DIR runs/ascii_pnm-gopkg_in_gographics_imagick_v3_imagick-replay
python3 parsarium.py afl build ascii_pnm go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py afl prepare ascii_pnm go gopkg_in_gographics_imagick_v3_imagick runs/ascii_pnm-gopkg_in_gographics_imagick_v3_imagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
