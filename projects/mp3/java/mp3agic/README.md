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

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign. The harness uses mp3agic's documented `Mp3File(Path)` local-file parser and reports only independently correct MPEG header fields.

**Coverage limit:** On the valid MPEG-2 control, `Mp3File(Path)` reports start byte 104, 5 frames, and 261 ms; the independent header walker finds start byte zero, 12 frames, and approximately 313 ms. Those inaccurate fields and PCM decoding are outside this path's claimed result.
