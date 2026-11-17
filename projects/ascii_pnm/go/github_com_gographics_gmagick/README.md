# github.com/gographics/gmagick — ASCII PNM / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/github-com-gographics-gmagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go github_com_gographics_gmagick
python3 parsarium.py run ascii_pnm go github_com_gographics_gmagick controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go github_com_gographics_gmagick CORPUS_DIR runs/ascii_pnm-github_com_gographics_gmagick-replay
python3 parsarium.py afl build ascii_pnm go github_com_gographics_gmagick
python3 parsarium.py afl prepare ascii_pnm go github_com_gographics_gmagick runs/ascii_pnm-github_com_gographics_gmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Only two valid ASCII controls (P3 PPM and P2 PGM, 2x1, maxval 255); GraphicsMagick 1.3.49 is built static from the pinned release tarball with delegates, modules and OpenMP disabled. No malformed input, fuzzing campaign, binary P4-P6 or PAM validation.
