# yoya/php-svg — SVG / PHP

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/yoya-php-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php yoya_php_svg
python3 parsarium.py run svg php yoya_php_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php yoya_php_svg CORPUS_DIR runs/svg-yoya_php_svg-replay
python3 parsarium.py afl build svg php yoya_php_svg
python3 parsarium.py afl prepare svg php yoya_php_svg runs/svg-yoya_php_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
