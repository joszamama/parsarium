# phil/svg-sanitizer — SVG / PHP

Pinned release: `0.1.0-alpha`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/phil-svg-sanitizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php phil_svg_sanitizer
python3 parsarium.py run svg php phil_svg_sanitizer controls/svg/red-green.svg
python3 parsarium.py replay svg php phil_svg_sanitizer CORPUS_DIR runs/svg-phil_svg_sanitizer-replay
python3 parsarium.py afl build svg php phil_svg_sanitizer
python3 parsarium.py afl prepare svg php phil_svg_sanitizer runs/svg-phil_svg_sanitizer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
