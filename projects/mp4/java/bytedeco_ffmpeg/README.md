# bytedeco-ffmpeg — MP4 / Java

Pinned release: `8.1.2-1.5.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/bytedeco-ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java bytedeco_ffmpeg
python3 parsarium.py run mp4 java bytedeco_ffmpeg controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java bytedeco_ffmpeg CORPUS_DIR runs/mp4-bytedeco_ffmpeg-replay
python3 parsarium.py afl build mp4 java bytedeco_ffmpeg
python3 parsarium.py afl prepare mp4 java bytedeco_ffmpeg runs/mp4-bytedeco_ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
