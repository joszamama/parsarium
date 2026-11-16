# league/glide — PNG / PHP

Pinned release: `4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/league-glide/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php league_glide
python3 parsarium.py run png php league_glide controls/png/red-green.png
python3 parsarium.py replay png php league_glide CORPUS_DIR runs/png-league_glide-replay
python3 parsarium.py afl build png php league_glide
python3 parsarium.py afl prepare png php league_glide runs/png-league_glide-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
