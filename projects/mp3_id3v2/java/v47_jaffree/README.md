# v47-jaffree — MP3 with ID3v2 / Java

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/java/v47-jaffree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 java v47_jaffree
python3 parsarium.py run mp3_id3v2 java v47_jaffree controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 java v47_jaffree CORPUS_DIR runs/mp3_id3v2-v47_jaffree-replay
python3 parsarium.py afl build mp3_id3v2 java v47_jaffree
python3 parsarium.py afl prepare mp3_id3v2 java v47_jaffree runs/mp3_id3v2-v47_jaffree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
