# symphonia-bundle-mp3 — MP3 / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/symphonia-bundle-mp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 rust symphonia_bundle_mp3
python3 parsarium.py run mp3 rust symphonia_bundle_mp3 controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 rust symphonia_bundle_mp3 CORPUS_DIR runs/mp3-symphonia_bundle_mp3-replay
python3 parsarium.py afl build mp3 rust symphonia_bundle_mp3
python3 parsarium.py afl prepare mp3 rust symphonia_bundle_mp3 runs/mp3-symphonia_bundle_mp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
