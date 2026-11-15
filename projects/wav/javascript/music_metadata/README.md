# music-metadata — WAV / JavaScript

Pinned release: `12.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/music-metadata/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript music_metadata
python3 parsarium.py run wav javascript music_metadata controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript music_metadata CORPUS_DIR runs/wav-music_metadata-replay
python3 parsarium.py afl build wav javascript music_metadata
python3 parsarium.py afl prepare wav javascript music_metadata runs/wav-music_metadata-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
