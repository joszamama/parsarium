# mp3-duration — plain MP3 / JavaScript

Pinned 1.1.0, with direct local-Buffer input, Docker control replay, V8 package-source coverage, and an opt-in AFL++ frame-count execution bridge. The same package/release is used in the MP3-with-ID3v2 cell; this path verifies untagged MPEG frame walking.

[Manifest](manifest.json) · [source lock](source-lock.json) · [control receipt](verification.json) · [API, results, and limits](../../../../catalog/mp3/javascript/mp3_duration/README.md)

Run from the repository root:

```sh
python3 parsarium.py build mp3 javascript mp3_duration
python3 parsarium.py run mp3 javascript mp3_duration controls/mp3/tone-44k-mono.mp3
python3 parsarium.py run mp3 javascript mp3_duration controls/mp3/tone-22k-stereo.mp3
python3 parsarium.py replay mp3 javascript mp3_duration CORPUS_DIR runs/mp3-mp3-duration-replay
python3 parsarium.py afl build mp3 javascript mp3_duration
python3 parsarium.py afl prepare mp3 javascript mp3_duration runs/mp3-mp3-duration-afl
```
