# v47-jaffree — MP4 / Java

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/v47-jaffree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java v47_jaffree
python3 parsarium.py run mp4 java v47_jaffree controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java v47_jaffree CORPUS_DIR runs/mp4-v47_jaffree-replay
python3 parsarium.py afl build mp4 java v47_jaffree
python3 parsarium.py afl prepare mp4 java v47_jaffree runs/mp4-v47_jaffree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
