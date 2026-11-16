# probe-image-size — PNG / JavaScript

Pinned release: `7.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/probe-image-size/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript probe_image_size
python3 parsarium.py run png javascript probe_image_size controls/png/red-green.png
python3 parsarium.py replay png javascript probe_image_size CORPUS_DIR runs/png-probe_image_size-replay
python3 parsarium.py afl build png javascript probe_image_size
python3 parsarium.py afl prepare png javascript probe_image_size runs/png-probe_image_size-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
