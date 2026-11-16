# audio-file — MP3 with ID3v2 / Rust

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/rust/audio-file/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 rust audio_file
python3 parsarium.py run mp3_id3v2 rust audio_file controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 rust audio_file CORPUS_DIR runs/mp3_id3v2-audio_file-replay
python3 parsarium.py afl build mp3_id3v2 rust audio_file
python3 parsarium.py afl prepare mp3_id3v2 rust audio_file runs/mp3_id3v2-audio_file-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
