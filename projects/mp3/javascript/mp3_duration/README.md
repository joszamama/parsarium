# mp3-duration — MP3 / JavaScript

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/mp3-duration/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript mp3_duration
python3 parsarium.py run mp3 javascript mp3_duration controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 javascript mp3_duration CORPUS_DIR runs/mp3-mp3_duration-replay
python3 parsarium.py afl build mp3 javascript mp3_duration
python3 parsarium.py afl prepare mp3 javascript mp3_duration runs/mp3-mp3_duration-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
