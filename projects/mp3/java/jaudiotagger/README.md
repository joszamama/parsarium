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

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign. This harness parses the first four-byte MPEG Layer III frame header at byte zero. It reports only verified header fields and does not decode the stream.

**Coverage limit:** On the valid MPEG-2 control, jaudiotagger's higher-level `MP3AudioHeader(File)` reports start byte 104 and five estimated frames, while the independent oracle records start byte zero and 12 frames. The selected low-level header API reports correct version, layer, rate, channels, and bitrate. Frame size, sample count, duration, and whole-stream frame count are outside the claimed result.
