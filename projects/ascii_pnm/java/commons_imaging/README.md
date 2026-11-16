# commons-imaging — ASCII PNM / Java

Pinned release: `1.0.0-alpha6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/commons-imaging/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java commons_imaging
python3 parsarium.py run ascii_pnm java commons_imaging controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java commons_imaging CORPUS_DIR runs/ascii_pnm-commons_imaging-replay
python3 parsarium.py afl build ascii_pnm java commons_imaging
python3 parsarium.py afl prepare ascii_pnm java commons_imaging runs/ascii_pnm-commons_imaging-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
