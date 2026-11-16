# truezip-utils — ZIP / Java

Pinned release: `1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/truezip-utils/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java truezip_utils
python3 parsarium.py run zip java truezip_utils controls/zip/hello.zip
python3 parsarium.py replay zip java truezip_utils CORPUS_DIR runs/zip-truezip_utils-replay
python3 parsarium.py afl build zip java truezip_utils
python3 parsarium.py afl prepare zip java truezip_utils runs/zip-truezip_utils-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
