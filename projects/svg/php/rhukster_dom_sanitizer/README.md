# rhukster/dom-sanitizer — SVG / PHP

Pinned release: `1.0.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/rhukster-dom-sanitizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php rhukster_dom_sanitizer
python3 parsarium.py run svg php rhukster_dom_sanitizer controls/svg/red-green.svg
python3 parsarium.py replay svg php rhukster_dom_sanitizer CORPUS_DIR runs/svg-rhukster_dom_sanitizer-replay
python3 parsarium.py afl build svg php rhukster_dom_sanitizer
python3 parsarium.py afl prepare svg php rhukster_dom_sanitizer runs/svg-rhukster_dom_sanitizer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
