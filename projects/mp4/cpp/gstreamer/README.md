# gstreamer — MP4 / C++

Pinned release: `1.28.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/gstreamer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp gstreamer
python3 parsarium.py run mp4 cpp gstreamer controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp gstreamer CORPUS_DIR runs/mp4-gstreamer-replay
python3 parsarium.py afl build mp4 cpp gstreamer
python3 parsarium.py afl prepare mp4 cpp gstreamer runs/mp4-gstreamer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
