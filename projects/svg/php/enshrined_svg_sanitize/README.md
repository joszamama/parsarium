# enshrined/svg-sanitize — SVG / PHP

Pinned release: `1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/enshrined-svg-sanitize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php enshrined_svg_sanitize
python3 parsarium.py run svg php enshrined_svg_sanitize controls/svg/red-green.svg
python3 parsarium.py replay svg php enshrined_svg_sanitize CORPUS_DIR runs/svg-enshrined_svg_sanitize-replay
python3 parsarium.py afl build svg php enshrined_svg_sanitize
python3 parsarium.py afl prepare svg php enshrined_svg_sanitize runs/svg-enshrined_svg_sanitize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
