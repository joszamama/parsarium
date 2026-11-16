# libmp4tag — MP4 / C++

Pinned release: `2.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/libmp4tag/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp libmp4tag
python3 parsarium.py run mp4 cpp libmp4tag controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp libmp4tag CORPUS_DIR runs/mp4-libmp4tag-replay
python3 parsarium.py afl build mp4 cpp libmp4tag
python3 parsarium.py afl prepare mp4 cpp libmp4tag runs/mp4-libmp4tag-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
