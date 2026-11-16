# oxiarc-archive — ZIP / Rust

Pinned release: `0.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/oxiarc-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust oxiarc_archive
python3 parsarium.py run zip rust oxiarc_archive controls/zip/hello.zip
python3 parsarium.py replay zip rust oxiarc_archive CORPUS_DIR runs/zip-oxiarc_archive-replay
python3 parsarium.py afl build zip rust oxiarc_archive
python3 parsarium.py afl prepare zip rust oxiarc_archive runs/zip-oxiarc_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
