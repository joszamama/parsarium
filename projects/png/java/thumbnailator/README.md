# thumbnailator — PNG / Java

Pinned release: `0.4.21`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/thumbnailator/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java thumbnailator
python3 parsarium.py run png java thumbnailator controls/png/red-green.png
python3 parsarium.py replay png java thumbnailator CORPUS_DIR runs/png-thumbnailator-replay
python3 parsarium.py afl build png java thumbnailator
python3 parsarium.py afl prepare png java thumbnailator runs/png-thumbnailator-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
