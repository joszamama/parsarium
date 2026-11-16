# bramp-ffmpeg — WAV / Java

Pinned release: `0.9.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/bramp-ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java bramp_ffmpeg
python3 parsarium.py run wav java bramp_ffmpeg controls/wav/256-samples.wav
python3 parsarium.py replay wav java bramp_ffmpeg CORPUS_DIR runs/wav-bramp_ffmpeg-replay
python3 parsarium.py afl build wav java bramp_ffmpeg
python3 parsarium.py afl prepare wav java bramp_ffmpeg runs/wav-bramp_ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
