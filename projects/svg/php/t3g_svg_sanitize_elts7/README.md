# t3g/svg-sanitize-elts7 — SVG / PHP

Pinned release: `0.15.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/t3g-svg-sanitize-elts7/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php t3g_svg_sanitize_elts7
python3 parsarium.py run svg php t3g_svg_sanitize_elts7 controls/svg/red-green.svg
python3 parsarium.py replay svg php t3g_svg_sanitize_elts7 CORPUS_DIR runs/svg-t3g_svg_sanitize_elts7-replay
python3 parsarium.py afl build svg php t3g_svg_sanitize_elts7
python3 parsarium.py afl prepare svg php t3g_svg_sanitize_elts7 runs/svg-t3g_svg_sanitize_elts7-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
