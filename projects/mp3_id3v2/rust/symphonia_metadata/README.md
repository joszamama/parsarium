# symphonia-metadata — MP3 / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/symphonia-metadata/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 rust symphonia_metadata
python3 parsarium.py run mp3_id3v2 rust symphonia_metadata controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 rust symphonia_metadata CORPUS_DIR runs/mp3_id3v2-symphonia_metadata-replay
python3 parsarium.py afl build mp3_id3v2 rust symphonia_metadata
python3 parsarium.py afl prepare mp3_id3v2 rust symphonia_metadata runs/mp3_id3v2-symphonia_metadata-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
