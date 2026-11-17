# symphonia — MP3 / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/symphonia/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 rust symphonia
python3 parsarium.py run mp3 rust symphonia controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 rust symphonia CORPUS_DIR runs/mp3-symphonia-replay
python3 parsarium.py afl build mp3 rust symphonia
python3 parsarium.py afl prepare mp3 rust symphonia runs/mp3-symphonia-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Facade over the same Symphonia MP3 demuxer/decoder as symphonia-bundle-mp3; not an independent parser family. Own coverage is the facade's registry and probe wiring only. Untagged CBR MPEG Layer III controls only; no VBR, Xing/Info, tags, free-format, Layer I/II, MPEG-2.5 or malformed input tested.
