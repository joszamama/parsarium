# ffmpeg — WAV / C

Pinned release: `9.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c ffmpeg
python3 parsarium.py run wav c ffmpeg controls/wav/four-samples.wav
python3 parsarium.py replay wav c ffmpeg CORPUS_DIR runs/wav-ffmpeg-replay
python3 parsarium.py afl build wav c ffmpeg
python3 parsarium.py afl prepare wav c ffmpeg runs/wav-ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
