# james-heinrich/getid3 — MP3 / PHP

Pinned release: `v1.9.28`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/james-heinrich-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 php getid3
python3 parsarium.py run mp3 php getid3 controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 php getid3 CORPUS_DIR runs/mp3-getid3-replay
python3 parsarium.py afl build mp3 php getid3
python3 parsarium.py afl prepare mp3 php getid3 runs/mp3-getid3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only. getID3 reads the first frame header, checks frame sync on following frames, and derives CBR duration from audio-data bytes and header bitrate; it does not decode audio or count every frame. Two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support. getID3 is also counted under mp3_id3v2/php for ID3v2 scope; this path is the plain-frame scope.
