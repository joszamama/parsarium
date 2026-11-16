# commons-vfs2 — ZIP / Java

Pinned release: `2.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/commons-vfs2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java commons_vfs2
python3 parsarium.py run zip java commons_vfs2 controls/zip/hello.zip
python3 parsarium.py replay zip java commons_vfs2 CORPUS_DIR runs/zip-commons_vfs2-replay
python3 parsarium.py afl build zip java commons_vfs2
python3 parsarium.py afl prepare zip java commons_vfs2 runs/zip-commons_vfs2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
