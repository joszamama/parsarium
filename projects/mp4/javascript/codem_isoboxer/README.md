# codem-isoboxer — MP4 / JavaScript

Pinned release: `0.3.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/codem-isoboxer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript codem_isoboxer
python3 parsarium.py run mp4 javascript codem_isoboxer controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript codem_isoboxer CORPUS_DIR runs/mp4-codem_isoboxer-replay
python3 parsarium.py afl build mp4 javascript codem_isoboxer
python3 parsarium.py afl prepare mp4 javascript codem_isoboxer runs/mp4-codem_isoboxer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
