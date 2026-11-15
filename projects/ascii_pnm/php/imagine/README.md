# imagine/imagine — ASCII PNM / PHP

Pinned release: `1.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/imagine-imagine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php imagine
python3 parsarium.py run ascii_pnm php imagine controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php imagine CORPUS_DIR runs/ascii_pnm-imagine-replay
python3 parsarium.py afl build ascii_pnm php imagine
python3 parsarium.py afl prepare ascii_pnm php imagine runs/ascii_pnm-imagine-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
