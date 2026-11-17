# github.com/cshum/vipsgen/vips — ASCII PNM / Go

Pinned release: `v1.3.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/github-com-cshum-vipsgen-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go github_com_cshum_vipsgen_vips
python3 parsarium.py run ascii_pnm go github_com_cshum_vipsgen_vips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go github_com_cshum_vipsgen_vips CORPUS_DIR runs/ascii_pnm-github_com_cshum_vipsgen_vips-replay
python3 parsarium.py afl build ascii_pnm go github_com_cshum_vipsgen_vips
python3 parsarium.py afl prepare ascii_pnm go github_com_cshum_vipsgen_vips runs/ascii_pnm-github_com_cshum_vipsgen_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Only two valid ASCII controls (P3 PPM and P2 PGM, 2x1, maxval 255); libvips 8.18.7 is built static from the pinned release tarball with every optional feature disabled except the PPM loader, cache disabled and concurrency 1. No malformed input, fuzzing campaign, binary P4-P6, PFM or PAM validation.
