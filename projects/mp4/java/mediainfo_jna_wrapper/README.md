# mediainfo-jna-wrapper — MP4 / Java

Pinned release: `2.1.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/mediainfo-jna-wrapper/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java mediainfo_jna_wrapper
python3 parsarium.py run mp4 java mediainfo_jna_wrapper controls/mp4/red-av-padded.mp4
python3 parsarium.py replay mp4 java mediainfo_jna_wrapper CORPUS_DIR runs/mp4-mediainfo_jna_wrapper-replay
python3 parsarium.py afl build mp4 java mediainfo_jna_wrapper
python3 parsarium.py afl prepare mp4 java mediainfo_jna_wrapper runs/mp4-mediainfo_jna_wrapper-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
