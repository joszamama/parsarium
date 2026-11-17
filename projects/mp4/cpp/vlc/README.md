# vlc — MP4 / C++

Pinned release: `3.0.24`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/vlc/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp vlc
python3 parsarium.py run mp4 cpp vlc controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp vlc CORPUS_DIR runs/mp4-vlc-replay
python3 parsarium.py afl build mp4 cpp vlc
python3 parsarium.py afl prepare mp4 cpp vlc runs/mp4-vlc-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
