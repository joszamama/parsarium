# music-metadata — MP3 / JavaScript

Pinned release: `12.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/music-metadata/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript music_metadata
python3 parsarium.py run mp3 javascript music_metadata controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 javascript music_metadata CORPUS_DIR runs/mp3-music_metadata-replay
python3 parsarium.py afl build mp3 javascript music_metadata
python3 parsarium.py afl prepare mp3 javascript music_metadata runs/mp3-music_metadata-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only; two valid CBR controls do not establish VBR, Xing/Info/LAME, free-format, Layer I/II, MPEG-2.5, ADTS, ID3 or CRC-protected support. MpegParser walks frame headers and skips side information; it does not decode audio. The harness passes `duration: true` so every frame is walked.
