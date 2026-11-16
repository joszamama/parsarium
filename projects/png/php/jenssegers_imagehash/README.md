# jenssegers/imagehash — PNG / PHP

Pinned release: `v0.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/jenssegers-imagehash/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php jenssegers_imagehash
python3 parsarium.py run png php jenssegers_imagehash controls/png/red-green.png
python3 parsarium.py replay png php jenssegers_imagehash CORPUS_DIR runs/png-jenssegers_imagehash-replay
python3 parsarium.py afl build png php jenssegers_imagehash
python3 parsarium.py afl prepare png php jenssegers_imagehash runs/png-jenssegers_imagehash-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
