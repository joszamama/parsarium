# minimp3_fixed — MP3 with ID3v2 / Rust

Pinned release: `0.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/rust/minimp3-fixed/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 rust minimp3_fixed
python3 parsarium.py run mp3_id3v2 rust minimp3_fixed controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 rust minimp3_fixed CORPUS_DIR runs/mp3_id3v2-minimp3_fixed-replay
python3 parsarium.py afl build mp3_id3v2 rust minimp3_fixed
python3 parsarium.py afl prepare mp3_id3v2 rust minimp3_fixed runs/mp3_id3v2-minimp3_fixed-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
