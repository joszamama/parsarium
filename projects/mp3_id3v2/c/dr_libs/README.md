# dr_libs — MP3 with ID3v2 / C

Pinned release: `mp3-0.7.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/c/dr-libs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 c dr_libs
python3 parsarium.py run mp3_id3v2 c dr_libs controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 c dr_libs CORPUS_DIR runs/mp3_id3v2-dr_libs-replay
python3 parsarium.py afl build mp3_id3v2 c dr_libs
python3 parsarium.py afl prepare mp3_id3v2 c dr_libs runs/mp3_id3v2-dr_libs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
