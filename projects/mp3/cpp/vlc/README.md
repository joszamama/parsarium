# vlc — MP3 / C++

Pinned release: `3.0.24`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/cpp/vlc/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 cpp vlc
python3 parsarium.py run mp3 cpp vlc controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 cpp vlc CORPUS_DIR runs/mp3-vlc-replay
python3 parsarium.py afl build mp3 cpp vlc
python3 parsarium.py afl prepare mp3 cpp vlc runs/mp3-vlc-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
