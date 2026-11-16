# mp4-stream — MP4 / JavaScript

Pinned release: `3.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/mp4-stream/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript mp4_stream
python3 parsarium.py run mp4 javascript mp4_stream controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript mp4_stream CORPUS_DIR runs/mp4-mp4_stream-replay
python3 parsarium.py afl build mp4 javascript mp4_stream
python3 parsarium.py afl prepare mp4 javascript mp4_stream runs/mp4-mp4_stream-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
