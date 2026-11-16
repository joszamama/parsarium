# phpthumb/phpthumb — ASCII PNM / PHP

Pinned release: `2.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/phpthumb-phpthumb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php phpthumb_phpthumb
python3 parsarium.py run ascii_pnm php phpthumb_phpthumb controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php phpthumb_phpthumb CORPUS_DIR runs/ascii_pnm-phpthumb_phpthumb-replay
python3 parsarium.py afl build ascii_pnm php phpthumb_phpthumb
python3 parsarium.py afl prepare ascii_pnm php phpthumb_phpthumb runs/ascii_pnm-phpthumb_phpthumb-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
