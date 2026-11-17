# github.com/cshum/vipsgen/vips — ASCII PNM / Go

- **Pinned release:** `v1.3.11`
- **License:** MIT
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** libvips ppmload
- **Local input API:** `NewPpmloadBuffer([]byte, *PpmloadBufferOptions)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/cshum/vipsgen/vips@v1.3.11>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ],
  "width": 2
}
```

Native libvips 8.18.7 libvips/foreign/ppmload.c loader (libvips is LGPL-2.1-or-later) reached through the vipsgen generated cgo binding for libvips 8.18 (built static from the pinned release tarball in the project image). The zero-importer libvips bindings already in preten (bu, kirklin, perelin, robxyy, shiqiyue) use the same ppmload family; no other libvips path is selected in this cell.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_cshum_vipsgen_vips/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_cshum_vipsgen_vips
python3 parsarium.py run ascii_pnm go github_com_cshum_vipsgen_vips controls/ascii_pnm/red-green.ppm
```

**Coverage limit:** Only two valid ASCII controls (P3 PPM and P2 PGM, 2x1, maxval 255); libvips 8.18.7 is built static from the pinned release tarball with every optional feature disabled except the PPM loader, cache disabled and concurrency 1. No malformed input, fuzzing campaign, binary P4-P6, PFM or PAM validation.
