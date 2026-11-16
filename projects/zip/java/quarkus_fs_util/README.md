# quarkus-fs-util — ZIP / Java

Pinned release: `1.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/quarkus-fs-util/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java quarkus_fs_util
python3 parsarium.py run zip java quarkus_fs_util controls/zip/hello.zip
python3 parsarium.py replay zip java quarkus_fs_util CORPUS_DIR runs/zip-quarkus_fs_util-replay
python3 parsarium.py afl build zip java quarkus_fs_util
python3 parsarium.py afl prepare zip java quarkus_fs_util runs/zip-quarkus_fs_util-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
