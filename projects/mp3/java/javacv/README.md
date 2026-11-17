# javacv — MP3 / Java

Pinned release: `1.5.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/java/javacv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 java javacv
python3 parsarium.py run mp3 java javacv controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 java javacv CORPUS_DIR runs/mp3-javacv-replay
python3 parsarium.py afl build mp3 java javacv
python3 parsarium.py afl prepare mp3 java javacv runs/mp3-javacv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
