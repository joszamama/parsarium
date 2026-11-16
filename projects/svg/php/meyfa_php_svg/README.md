# meyfa/php-svg — SVG / PHP

Pinned release: `v0.16.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/meyfa-php-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php meyfa_php_svg
python3 parsarium.py run svg php meyfa_php_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php meyfa_php_svg CORPUS_DIR runs/svg-meyfa_php_svg-replay
python3 parsarium.py afl build svg php meyfa_php_svg
python3 parsarium.py afl prepare svg php meyfa_php_svg runs/svg-meyfa_php_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
