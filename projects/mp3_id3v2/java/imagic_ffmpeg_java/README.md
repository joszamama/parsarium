# imagic-ffmpeg-java — MP3 with ID3v2 / Java

Pinned release: `0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/java/imagic-ffmpeg-java/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 java imagic_ffmpeg_java
python3 parsarium.py run mp3_id3v2 java imagic_ffmpeg_java controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 java imagic_ffmpeg_java CORPUS_DIR runs/mp3_id3v2-imagic_ffmpeg_java-replay
python3 parsarium.py afl build mp3_id3v2 java imagic_ffmpeg_java
python3 parsarium.py afl prepare mp3_id3v2 java imagic_ffmpeg_java runs/mp3_id3v2-imagic_ffmpeg_java-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
