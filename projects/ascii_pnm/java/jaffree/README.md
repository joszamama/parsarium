# jaffree — ASCII PNM / Java

Pinned release: `2024.08.29`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/jaffree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java jaffree
python3 parsarium.py run ascii_pnm java jaffree controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java jaffree CORPUS_DIR runs/ascii_pnm-jaffree-replay
python3 parsarium.py afl build ascii_pnm java jaffree
python3 parsarium.py afl prepare ascii_pnm java jaffree runs/ascii_pnm-jaffree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
