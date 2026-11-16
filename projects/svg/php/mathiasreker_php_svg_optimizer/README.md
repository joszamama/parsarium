# mathiasreker/php-svg-optimizer — SVG / PHP

Pinned release: `10.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/mathiasreker-php-svg-optimizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php mathiasreker_php_svg_optimizer
python3 parsarium.py run svg php mathiasreker_php_svg_optimizer controls/svg/red-green.svg
python3 parsarium.py replay svg php mathiasreker_php_svg_optimizer CORPUS_DIR runs/svg-mathiasreker_php_svg_optimizer-replay
python3 parsarium.py afl build svg php mathiasreker_php_svg_optimizer
python3 parsarium.py afl prepare svg php mathiasreker_php_svg_optimizer runs/svg-mathiasreker_php_svg_optimizer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
