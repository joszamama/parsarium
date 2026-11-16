# league/color-extractor — PNG / PHP

Pinned release: `0.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/league-color-extractor/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php league_color_extractor
python3 parsarium.py run png php league_color_extractor controls/png/red-green.png
python3 parsarium.py replay png php league_color_extractor CORPUS_DIR runs/png-league_color_extractor-replay
python3 parsarium.py afl build png php league_color_extractor
python3 parsarium.py afl prepare png php league_color_extractor runs/png-league_color_extractor-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
