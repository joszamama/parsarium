# vlcj-info — MP3 with ID3v2 / Java

Pinned release: `2.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/java/vlcj-info/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 java vlcj_info
python3 parsarium.py run mp3_id3v2 java vlcj_info controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 java vlcj_info CORPUS_DIR runs/mp3_id3v2-vlcj_info-replay
python3 parsarium.py afl build mp3_id3v2 java vlcj_info
python3 parsarium.py afl prepare mp3_id3v2 java vlcj_info runs/mp3_id3v2-vlcj_info-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
