# league/flysystem-ziparchive — ZIP / PHP

Pinned release: `3.31.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/league-flysystem-ziparchive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php league_flysystem_ziparchive
python3 parsarium.py run zip php league_flysystem_ziparchive controls/zip/hello.zip
python3 parsarium.py replay zip php league_flysystem_ziparchive CORPUS_DIR runs/zip-league_flysystem_ziparchive-replay
python3 parsarium.py afl build zip php league_flysystem_ziparchive
python3 parsarium.py afl prepare zip php league_flysystem_ziparchive runs/zip-league_flysystem_ziparchive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
