# darylldoyle/safe-svg — SVG / PHP

Pinned release: `2.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/darylldoyle-safe-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php darylldoyle_safe_svg
python3 parsarium.py run svg php darylldoyle_safe_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php darylldoyle_safe_svg CORPUS_DIR runs/svg-darylldoyle_safe_svg-replay
python3 parsarium.py afl build svg php darylldoyle_safe_svg
python3 parsarium.py afl prepare svg php darylldoyle_safe_svg runs/svg-darylldoyle_safe_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
