# truevfs-driver-zip — ZIP / Java

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/truevfs-driver-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java truevfs_driver_zip
python3 parsarium.py run zip java truevfs_driver_zip controls/zip/hello.zip
python3 parsarium.py replay zip java truevfs_driver_zip CORPUS_DIR runs/zip-truevfs_driver_zip-replay
python3 parsarium.py afl build zip java truevfs_driver_zip
python3 parsarium.py afl prepare zip java truevfs_driver_zip runs/zip-truevfs_driver_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
