# rc-zip-sync — ZIP / Rust

Pinned release: `4.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/rc-zip-sync/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust rc_zip_sync
python3 parsarium.py run zip rust rc_zip_sync controls/zip/hello.zip
python3 parsarium.py replay zip rust rc_zip_sync CORPUS_DIR runs/zip-rc_zip_sync-replay
python3 parsarium.py afl build zip rust rc_zip_sync
python3 parsarium.py afl prepare zip rust rc_zip_sync runs/zip-rc_zip_sync-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
