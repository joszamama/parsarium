# @loaders.gl/ply — ASCII PLY / JavaScript

Pinned release: `4.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/loaders-gl-ply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript loaders_gl_ply
python3 parsarium.py run ascii_ply javascript loaders_gl_ply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript loaders_gl_ply CORPUS_DIR runs/ascii_ply-loaders_gl_ply-replay
python3 parsarium.py afl build ascii_ply javascript loaders_gl_ply
python3 parsarium.py afl prepare ascii_ply javascript loaders_gl_ply runs/ascii_ply-loaders_gl_ply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
