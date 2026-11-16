# tika-image — PNG / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/tika-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java tika_image
python3 parsarium.py run png java tika_image controls/png/red-green.png
python3 parsarium.py replay png java tika_image CORPUS_DIR runs/png-tika_image-replay
python3 parsarium.py afl build png java tika_image
python3 parsarium.py afl prepare png java tika_image runs/png-tika_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
