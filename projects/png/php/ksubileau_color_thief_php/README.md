# ksubileau/color-thief-php — PNG / PHP

Pinned release: `v3.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/ksubileau-color-thief-php/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php ksubileau_color_thief_php
python3 parsarium.py run png php ksubileau_color_thief_php controls/png/red-green.png
python3 parsarium.py replay png php ksubileau_color_thief_php CORPUS_DIR runs/png-ksubileau_color_thief_php-replay
python3 parsarium.py afl build png php ksubileau_color_thief_php
python3 parsarium.py afl prepare png php ksubileau_color_thief_php runs/png-ksubileau_color_thief_php-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
