# vlcj-info — MP4 / Java

Pinned release: `2.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/vlcj-info/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java vlcj_info
python3 parsarium.py run mp4 java vlcj_info controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java vlcj_info CORPUS_DIR runs/mp4-vlcj_info-replay
python3 parsarium.py afl build mp4 java vlcj_info
python3 parsarium.py afl prepare mp4 java vlcj_info runs/mp4-vlcj_info-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
