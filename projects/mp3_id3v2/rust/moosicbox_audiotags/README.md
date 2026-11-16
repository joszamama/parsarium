# moosicbox_audiotags — MP3 with ID3v2 / Rust

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/rust/moosicbox-audiotags/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 rust moosicbox_audiotags
python3 parsarium.py run mp3_id3v2 rust moosicbox_audiotags controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 rust moosicbox_audiotags CORPUS_DIR runs/mp3_id3v2-moosicbox_audiotags-replay
python3 parsarium.py afl build mp3_id3v2 rust moosicbox_audiotags
python3 parsarium.py afl prepare mp3_id3v2 rust moosicbox_audiotags runs/mp3_id3v2-moosicbox_audiotags-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
