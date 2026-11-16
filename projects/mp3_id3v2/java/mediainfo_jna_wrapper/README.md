# mediainfo-jna-wrapper — MP3 with ID3v2 / Java

Pinned release: `2.1.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/java/mediainfo-jna-wrapper/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 java mediainfo_jna_wrapper
python3 parsarium.py run mp3_id3v2 java mediainfo_jna_wrapper controls/mp3_id3v2/tone-tags-long.mp3
python3 parsarium.py replay mp3_id3v2 java mediainfo_jna_wrapper CORPUS_DIR runs/mp3_id3v2-mediainfo_jna_wrapper-replay
python3 parsarium.py afl build mp3_id3v2 java mediainfo_jna_wrapper
python3 parsarium.py afl prepare mp3_id3v2 java mediainfo_jna_wrapper runs/mp3_id3v2-mediainfo_jna_wrapper-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
