# gstreamer — WAV / C++

Pinned release: `1.28.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/gstreamer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp gstreamer
python3 parsarium.py run wav cpp gstreamer controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp gstreamer CORPUS_DIR runs/wav-gstreamer-replay
python3 parsarium.py afl build wav cpp gstreamer
python3 parsarium.py afl prepare wav cpp gstreamer runs/wav-gstreamer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
