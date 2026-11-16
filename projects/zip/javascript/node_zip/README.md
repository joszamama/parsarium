# node-zip — ZIP / JavaScript

Pinned release: `1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/node-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript node_zip
python3 parsarium.py run zip javascript node_zip controls/zip/hello.zip
python3 parsarium.py replay zip javascript node_zip CORPUS_DIR runs/zip-node_zip-replay
python3 parsarium.py afl build zip javascript node_zip
python3 parsarium.py afl prepare zip javascript node_zip runs/zip-node_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
