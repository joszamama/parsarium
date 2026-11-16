# @stacksjs/ts-svg — SVG / JavaScript

Pinned release: `0.1.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/stacksjs-ts-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript stacksjs_ts_svg
python3 parsarium.py run svg javascript stacksjs_ts_svg controls/svg/red-green.svg
python3 parsarium.py replay svg javascript stacksjs_ts_svg CORPUS_DIR runs/svg-stacksjs_ts_svg-replay
python3 parsarium.py afl build svg javascript stacksjs_ts_svg
python3 parsarium.py afl prepare svg javascript stacksjs_ts_svg runs/svg-stacksjs_ts_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
