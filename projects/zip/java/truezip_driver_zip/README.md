# truezip-driver-zip — ZIP / Java

Pinned release: `7.7.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/truezip-driver-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java truezip_driver_zip
python3 parsarium.py run zip java truezip_driver_zip controls/zip/hello.zip
python3 parsarium.py replay zip java truezip_driver_zip CORPUS_DIR runs/zip-truezip_driver_zip-replay
python3 parsarium.py afl build zip java truezip_driver_zip
python3 parsarium.py afl prepare zip java truezip_driver_zip runs/zip-truezip_driver_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
