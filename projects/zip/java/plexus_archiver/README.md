# plexus-archiver — ZIP / Java

Pinned release: `4.15.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/plexus-archiver/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java plexus_archiver
python3 parsarium.py run zip java plexus_archiver controls/zip/hello.zip
python3 parsarium.py replay zip java plexus_archiver CORPUS_DIR runs/zip-plexus_archiver-replay
python3 parsarium.py afl build zip java plexus_archiver
python3 parsarium.py afl prepare zip java plexus_archiver runs/zip-plexus_archiver-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
