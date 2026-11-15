# jaudiotagger — MP3 with ID3v2 / Java

Pinned release: `3.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/java/jaudiotagger/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 java jaudiotagger
python3 parsarium.py run mp3_id3v2 java jaudiotagger controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 java jaudiotagger CORPUS_DIR runs/mp3_id3v2-jaudiotagger-replay
python3 parsarium.py afl build mp3_id3v2 java jaudiotagger
python3 parsarium.py afl prepare mp3_id3v2 java jaudiotagger runs/mp3_id3v2-jaudiotagger-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
