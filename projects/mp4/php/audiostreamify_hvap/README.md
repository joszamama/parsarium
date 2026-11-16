# audiostreamify/hvap — MP4 / PHP

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/audiostreamify-hvap/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php audiostreamify_hvap
python3 parsarium.py run mp4 php audiostreamify_hvap controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php audiostreamify_hvap CORPUS_DIR runs/mp4-audiostreamify_hvap-replay
python3 parsarium.py afl build mp4 php audiostreamify_hvap
python3 parsarium.py afl prepare mp4 php audiostreamify_hvap runs/mp4-audiostreamify_hvap-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
