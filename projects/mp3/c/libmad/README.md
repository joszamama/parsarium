# libmad — MP3 / C

Pinned release: `0.16.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/c/libmad/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 c libmad
python3 parsarium.py run mp3 c libmad controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 c libmad CORPUS_DIR runs/mp3-libmad-replay
python3 parsarium.py afl build mp3 c libmad
python3 parsarium.py afl prepare mp3 c libmad runs/mp3-libmad-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only; two valid CBR controls (MPEG-1 44.1 kHz mono, MPEG-2 22.05 kHz stereo) do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 or ID3 handling. libmad is also linked by the SoX path counted under mp3_id3v2/c; this is its own plain-frame path. Fixed-point output is not compared sample by sample with another decoder.
