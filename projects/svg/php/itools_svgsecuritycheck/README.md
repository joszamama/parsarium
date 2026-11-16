# itools/svgsecuritycheck — SVG / PHP

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/itools-svgsecuritycheck/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php itools_svgsecuritycheck
python3 parsarium.py run svg php itools_svgsecuritycheck controls/svg/red-green.svg
python3 parsarium.py replay svg php itools_svgsecuritycheck CORPUS_DIR runs/svg-itools_svgsecuritycheck-replay
python3 parsarium.py afl build svg php itools_svgsecuritycheck
python3 parsarium.py afl prepare svg php itools_svgsecuritycheck runs/svg-itools_svgsecuritycheck-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
