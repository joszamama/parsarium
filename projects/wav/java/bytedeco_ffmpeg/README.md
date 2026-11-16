# bytedeco-ffmpeg — WAV / Java

Pinned release: `8.1.2-1.5.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/bytedeco-ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java bytedeco_ffmpeg
python3 parsarium.py run wav java bytedeco_ffmpeg controls/wav/256-samples.wav
python3 parsarium.py replay wav java bytedeco_ffmpeg CORPUS_DIR runs/wav-bytedeco_ffmpeg-replay
python3 parsarium.py afl build wav java bytedeco_ffmpeg
python3 parsarium.py afl prepare wav java bytedeco_ffmpeg runs/wav-bytedeco_ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
