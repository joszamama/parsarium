# ij — ASCII PNM / Java

Pinned release: `1.54p`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/ij/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java ij
python3 parsarium.py run ascii_pnm java ij controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java ij CORPUS_DIR runs/ascii_pnm-ij-replay
python3 parsarium.py afl build ascii_pnm java ij
python3 parsarium.py afl prepare ascii_pnm java ij runs/ascii_pnm-ij-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
