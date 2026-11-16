# node:zlib.ZipBuffer — ZIP / JavaScript

Pinned release: `26.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/javascript/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript stdlib_node_zipbuffer
python3 parsarium.py run zip javascript stdlib_node_zipbuffer controls/zip/hello.zip
python3 parsarium.py replay zip javascript stdlib_node_zipbuffer CORPUS_DIR runs/zip-stdlib_node_zipbuffer-replay
python3 parsarium.py afl build zip javascript stdlib_node_zipbuffer
python3 parsarium.py afl prepare zip javascript stdlib_node_zipbuffer runs/zip-stdlib_node_zipbuffer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** AFL++ maps bundled Node ZIP JavaScript modules; prebuilt native zlib decompression branches are outside this feedback.
