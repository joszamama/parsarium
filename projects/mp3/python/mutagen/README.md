# mutagen — MP3 / Python

Pinned release: `1.48.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/mutagen/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 python mutagen
python3 parsarium.py run mp3 python mutagen controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 python mutagen CORPUS_DIR runs/mp3-mutagen-replay
python3 parsarium.py afl build mp3 python mutagen
python3 parsarium.py afl prepare mp3 python mutagen runs/mp3-mutagen-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only. Mutagen reads the first frame header, checks following frame syncs, and looks for Xing/Info/VBRI; without them it estimates duration from stream bytes and the header bitrate. It does not decode audio. Two valid CBR controls do not establish VBR, free-format, Layer I/II, or MPEG-2.5 support. Same Mutagen package and mp3 module as the mp3_id3v2/python mutagen entry.
