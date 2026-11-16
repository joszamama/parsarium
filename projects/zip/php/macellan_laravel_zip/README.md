# macellan/laravel-zip — ZIP / PHP

Pinned release: `1.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/macellan-laravel-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php macellan_laravel_zip
python3 parsarium.py run zip php macellan_laravel_zip controls/zip/hello.zip
python3 parsarium.py replay zip php macellan_laravel_zip CORPUS_DIR runs/zip-macellan_laravel_zip-replay
python3 parsarium.py afl build zip php macellan_laravel_zip
python3 parsarium.py afl prepare zip php macellan_laravel_zip runs/zip-macellan_laravel_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
