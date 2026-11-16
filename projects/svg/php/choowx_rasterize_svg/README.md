# choowx/rasterize-svg — SVG / PHP

Pinned release: `v0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/choowx-rasterize-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php choowx_rasterize_svg
python3 parsarium.py run svg php choowx_rasterize_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php choowx_rasterize_svg CORPUS_DIR runs/svg-choowx_rasterize_svg-replay
python3 parsarium.py afl build svg php choowx_rasterize_svg
python3 parsarium.py afl prepare svg php choowx_rasterize_svg runs/svg-choowx_rasterize_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
