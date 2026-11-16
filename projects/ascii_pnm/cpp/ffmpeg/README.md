# ffmpeg — ASCII PNM / C++

Pinned release: `9.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/cpp/ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp ffmpeg
python3 parsarium.py run ascii_pnm cpp ffmpeg controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp ffmpeg CORPUS_DIR runs/ascii_pnm-ffmpeg-replay
python3 parsarium.py afl build ascii_pnm cpp ffmpeg
python3 parsarium.py afl prepare ascii_pnm cpp ffmpeg runs/ascii_pnm-ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
