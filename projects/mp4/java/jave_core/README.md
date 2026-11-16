# jave-core — MP4 / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/jave-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java jave_core
python3 parsarium.py run mp4 java jave_core controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java jave_core CORPUS_DIR runs/mp4-jave_core-replay
python3 parsarium.py afl build mp4 java jave_core
python3 parsarium.py afl prepare mp4 java jave_core runs/mp4-jave_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
