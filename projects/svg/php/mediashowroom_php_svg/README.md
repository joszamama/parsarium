# mediashowroom/php-svg — SVG / PHP

Pinned release: `v0.7.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/mediashowroom-php-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php mediashowroom_php_svg
python3 parsarium.py run svg php mediashowroom_php_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php mediashowroom_php_svg CORPUS_DIR runs/svg-mediashowroom_php_svg-replay
python3 parsarium.py afl build svg php mediashowroom_php_svg
python3 parsarium.py afl prepare svg php mediashowroom_php_svg runs/svg-mediashowroom_php_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
