# itext-svg — SVG / Java

Pinned release: `9.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/itext-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java itext_svg
python3 parsarium.py run svg java itext_svg controls/svg/red-green.svg
python3 parsarium.py replay svg java itext_svg CORPUS_DIR runs/svg-itext_svg-replay
python3 parsarium.py afl build svg java itext_svg
python3 parsarium.py afl prepare svg java itext_svg runs/svg-itext_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
