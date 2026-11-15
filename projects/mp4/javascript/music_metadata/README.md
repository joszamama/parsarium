# music-metadata — MP4 / JavaScript

Pinned release: `12.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/music-metadata/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript music_metadata
python3 parsarium.py run mp4 javascript music_metadata controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript music_metadata CORPUS_DIR runs/mp4-music_metadata-replay
python3 parsarium.py afl build mp4 javascript music_metadata
python3 parsarium.py afl prepare mp4 javascript music_metadata runs/mp4-music_metadata-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
