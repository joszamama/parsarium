# mp3agic — MP3 / Java

Pinned release: `0.9.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/java/mp3agic/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 java mp3agic
python3 parsarium.py run mp3 java mp3agic controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 java mp3agic CORPUS_DIR runs/mp3-mp3agic-replay
python3 parsarium.py afl build mp3 java mp3agic
python3 parsarium.py afl prepare mp3 java mp3agic runs/mp3-mp3agic-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid untagged CBR MPEG Layer III files; only independently correct version, layer, sample rate, channel mode and bitrate are claimed. Mp3File(Path) misidentifies the 22.05 kHz control start at byte 104 and reports 5 frames/261 ms versus oracle byte 0, 12 frames/about 313 ms. No accurate whole-stream frame count, duration or PCM decoding claim; VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 and ID3 are untested.
