# jaudiotagger — MP3 / Java

Pinned release: `3.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/java/jaudiotagger/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 java jaudiotagger
python3 parsarium.py run mp3 java jaudiotagger controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 java jaudiotagger CORPUS_DIR runs/mp3-jaudiotagger-replay
python3 parsarium.py afl build mp3 java jaudiotagger
python3 parsarium.py afl prepare mp3 java jaudiotagger runs/mp3-jaudiotagger-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** First four-byte frame header of two valid untagged CBR MPEG Layer III files only; no frame count, frame size, duration, whole-stream consistency, PCM decode, ID3, VBR, or malformed-input claim. The higher-level MP3AudioHeader(File) misidentifies the valid 22.05 kHz control start at byte 104 and estimates 5 rather than 12 frames; MPEGFrameHeader.getFrameLength/getNoOfSamples are also wrong for that MPEG-2 header and are not reported.
