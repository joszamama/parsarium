# imagic-ffmpeg-java — MP4 / Java

Pinned release: `0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/imagic-ffmpeg-java/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java imagic_ffmpeg_java
python3 parsarium.py run mp4 java imagic_ffmpeg_java controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java imagic_ffmpeg_java CORPUS_DIR runs/mp4-imagic_ffmpeg_java-replay
python3 parsarium.py afl build mp4 java imagic_ffmpeg_java
python3 parsarium.py afl prepare mp4 java imagic_ffmpeg_java runs/mp4-imagic_ffmpeg_java-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
