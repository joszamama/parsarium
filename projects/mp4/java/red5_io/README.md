# red5-io — MP4 / Java

Pinned release: `2.0.40`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/red5-io/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java red5_io
python3 parsarium.py run mp4 java red5_io controls/mp4/red-av-3s.mp4
python3 parsarium.py replay mp4 java red5_io CORPUS_DIR runs/mp4-red5_io-replay
python3 parsarium.py afl build mp4 java red5_io
python3 parsarium.py afl prepare mp4 java red5_io runs/mp4-red5_io-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
