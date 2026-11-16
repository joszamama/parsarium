# jave-core — ASCII PNM / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/jave-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java jave_core
python3 parsarium.py run ascii_pnm java jave_core controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java jave_core CORPUS_DIR runs/ascii_pnm-jave_core-replay
python3 parsarium.py afl build ascii_pnm java jave_core
python3 parsarium.py afl prepare ascii_pnm java jave_core runs/ascii_pnm-jave_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
