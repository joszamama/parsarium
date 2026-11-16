# @loaders.gl/zip — ZIP / JavaScript

Pinned release: `4.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/loaders-gl-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript loaders_gl_zip
python3 parsarium.py run zip javascript loaders_gl_zip controls/zip/hello.zip
python3 parsarium.py replay zip javascript loaders_gl_zip CORPUS_DIR runs/zip-loaders_gl_zip-replay
python3 parsarium.py afl build zip javascript loaders_gl_zip
python3 parsarium.py afl prepare zip javascript loaders_gl_zip runs/zip-loaders_gl_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
