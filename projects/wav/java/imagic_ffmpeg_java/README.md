# imagic-ffmpeg-java — WAV / Java

Pinned release: `0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/imagic-ffmpeg-java/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java imagic_ffmpeg_java
python3 parsarium.py run wav java imagic_ffmpeg_java controls/wav/256-samples.wav
python3 parsarium.py replay wav java imagic_ffmpeg_java CORPUS_DIR runs/wav-imagic_ffmpeg_java-replay
python3 parsarium.py afl build wav java imagic_ffmpeg_java
python3 parsarium.py afl prepare wav java imagic_ffmpeg_java runs/wav-imagic_ffmpeg_java-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
