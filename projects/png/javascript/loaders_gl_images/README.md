# @loaders.gl/images — PNG / JavaScript

Pinned release: `4.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/loaders-gl-images/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript loaders_gl_images
python3 parsarium.py run png javascript loaders_gl_images controls/png/red-green.png
python3 parsarium.py replay png javascript loaders_gl_images CORPUS_DIR runs/png-loaders_gl_images-replay
python3 parsarium.py afl build png javascript loaders_gl_images
python3 parsarium.py afl prepare png javascript loaders_gl_images runs/png-loaders_gl_images-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
