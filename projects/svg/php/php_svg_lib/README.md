# dompdf/php-svg-lib — SVG / PHP

Pinned release: `1.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/dompdf-php-svg-lib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php php_svg_lib
python3 parsarium.py run svg php php_svg_lib controls/svg/red-green.svg
python3 parsarium.py replay svg php php_svg_lib CORPUS_DIR runs/svg-php_svg_lib-replay
python3 parsarium.py afl build svg php php_svg_lib
python3 parsarium.py afl prepare svg php php_svg_lib runs/svg-php_svg_lib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
