# decmuc/svgsanitizer — SVG / PHP

Pinned release: `v1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/decmuc-svgsanitizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php decmuc_svgsanitizer
python3 parsarium.py run svg php decmuc_svgsanitizer controls/svg/red-green.svg
python3 parsarium.py replay svg php decmuc_svgsanitizer CORPUS_DIR runs/svg-decmuc_svgsanitizer-replay
python3 parsarium.py afl build svg php decmuc_svgsanitizer
python3 parsarium.py afl prepare svg php decmuc_svgsanitizer runs/svg-decmuc_svgsanitizer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
