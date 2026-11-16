# mgrulich/php-svg-lib — SVG / PHP

Pinned release: `v0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/mgrulich-php-svg-lib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php mgrulich_php_svg_lib
python3 parsarium.py run svg php mgrulich_php_svg_lib controls/svg/red-green.svg
python3 parsarium.py replay svg php mgrulich_php_svg_lib CORPUS_DIR runs/svg-mgrulich_php_svg_lib-replay
python3 parsarium.py afl build svg php mgrulich_php_svg_lib
python3 parsarium.py afl prepare svg php mgrulich_php_svg_lib runs/svg-mgrulich_php_svg_lib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
