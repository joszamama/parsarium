# node-id3 — MP3 / JavaScript

Pinned release: `0.2.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/node-id3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript node_id3
python3 parsarium.py run mp3_id3v2 javascript node_id3 controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript node_id3 CORPUS_DIR runs/mp3_id3v2-node_id3-replay
python3 parsarium.py afl build mp3_id3v2 javascript node_id3
python3 parsarium.py afl prepare mp3_id3v2 javascript node_id3 runs/mp3_id3v2-node_id3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
