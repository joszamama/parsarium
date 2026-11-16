# imagefmt — PNG / Rust

Pinned release: `4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/imagefmt/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust imagefmt
python3 parsarium.py run png rust imagefmt controls/png/red-green.png
python3 parsarium.py replay png rust imagefmt CORPUS_DIR runs/png-imagefmt-replay
python3 parsarium.py afl build png rust imagefmt
python3 parsarium.py afl prepare png rust imagefmt runs/png-imagefmt-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
