# pb-imgsize — PNG / Rust

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/pb-imgsize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust pb_imgsize
python3 parsarium.py run png rust pb_imgsize controls/png/red-green.png
python3 parsarium.py replay png rust pb_imgsize CORPUS_DIR runs/png-pb_imgsize-replay
python3 parsarium.py afl build png rust pb_imgsize
python3 parsarium.py afl prepare png rust pb_imgsize runs/png-pb_imgsize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
