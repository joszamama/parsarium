# commons-imaging — PNG / Java

Pinned release: `1.0.0-alpha6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/commons-imaging/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java commons_imaging
python3 parsarium.py run png java commons_imaging controls/png/red-green.png
python3 parsarium.py replay png java commons_imaging CORPUS_DIR runs/png-commons_imaging-replay
python3 parsarium.py afl build png java commons_imaging
python3 parsarium.py afl prepare png java commons_imaging runs/png-commons_imaging-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
