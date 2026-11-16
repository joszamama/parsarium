# league/glide — ASCII PNM / PHP

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/league-glide/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php league_glide
python3 parsarium.py run ascii_pnm php league_glide controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php league_glide CORPUS_DIR runs/ascii_pnm-league_glide-replay
python3 parsarium.py afl build ascii_pnm php league_glide
python3 parsarium.py afl prepare ascii_pnm php league_glide runs/ascii_pnm-league_glide-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
