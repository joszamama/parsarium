# bytedeco-ffmpeg — ASCII PNM / Java

Pinned release: `8.1.2-1.5.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/bytedeco-ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java bytedeco_ffmpeg
python3 parsarium.py run ascii_pnm java bytedeco_ffmpeg controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java bytedeco_ffmpeg CORPUS_DIR runs/ascii_pnm-bytedeco_ffmpeg-replay
python3 parsarium.py afl build ascii_pnm java bytedeco_ffmpeg
python3 parsarium.py afl prepare ascii_pnm java bytedeco_ffmpeg runs/ascii_pnm-bytedeco_ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
