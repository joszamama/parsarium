# bytedeco-ffmpeg — MP3 with ID3v2 / Java

Pinned release: `8.1.2-1.5.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/java/bytedeco-ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 java bytedeco_ffmpeg
python3 parsarium.py run mp3_id3v2 java bytedeco_ffmpeg controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 java bytedeco_ffmpeg CORPUS_DIR runs/mp3_id3v2-bytedeco_ffmpeg-replay
python3 parsarium.py afl build mp3_id3v2 java bytedeco_ffmpeg
python3 parsarium.py afl prepare mp3_id3v2 java bytedeco_ffmpeg runs/mp3_id3v2-bytedeco_ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
