# openpnp-opencv — PNG / Java

Pinned release: `4.9.0-0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/openpnp-opencv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java openpnp_opencv
python3 parsarium.py run png java openpnp_opencv controls/png/red-green.png
python3 parsarium.py replay png java openpnp_opencv CORPUS_DIR runs/png-openpnp_opencv-replay
python3 parsarium.py afl build png java openpnp_opencv
python3 parsarium.py afl prepare png java openpnp_opencv runs/png-openpnp_opencv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
