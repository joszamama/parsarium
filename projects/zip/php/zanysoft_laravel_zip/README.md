# zanysoft/laravel-zip — ZIP / PHP

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/zanysoft-laravel-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php zanysoft_laravel_zip
python3 parsarium.py run zip php zanysoft_laravel_zip controls/zip/hello.zip
python3 parsarium.py replay zip php zanysoft_laravel_zip CORPUS_DIR runs/zip-zanysoft_laravel_zip-replay
python3 parsarium.py afl build zip php zanysoft_laravel_zip
python3 parsarium.py afl prepare zip php zanysoft_laravel_zip runs/zip-zanysoft_laravel_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
