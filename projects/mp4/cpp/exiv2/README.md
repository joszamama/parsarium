# exiv2 — MP4 / C++

Pinned release: `0.28.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/exiv2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp exiv2
python3 parsarium.py run mp4 cpp exiv2 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp exiv2 CORPUS_DIR runs/mp4-exiv2-replay
python3 parsarium.py afl build mp4 cpp exiv2
python3 parsarium.py afl prepare mp4 cpp exiv2 runs/mp4-exiv2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
