# isobmff-inspector — MP4 / JavaScript

Pinned release: `0.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/isobmff-inspector/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript isobmff_inspector
python3 parsarium.py run mp4 javascript isobmff_inspector controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript isobmff_inspector CORPUS_DIR runs/mp4-isobmff_inspector-replay
python3 parsarium.py afl build mp4 javascript isobmff_inspector
python3 parsarium.py afl prepare mp4 javascript isobmff_inspector runs/mp4-isobmff_inspector-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
