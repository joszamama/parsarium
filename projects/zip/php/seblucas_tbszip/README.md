# seblucas/tbszip — ZIP / PHP

Pinned release: `2.16.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/seblucas-tbszip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php seblucas_tbszip
python3 parsarium.py run zip php seblucas_tbszip controls/zip/hello.zip
python3 parsarium.py replay zip php seblucas_tbszip CORPUS_DIR runs/zip-seblucas_tbszip-replay
python3 parsarium.py afl build zip php seblucas_tbszip
python3 parsarium.py afl prepare zip php seblucas_tbszip runs/zip-seblucas_tbszip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
