# imagic-ffmpeg-java — ASCII PNM / Java

Pinned release: `0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/imagic-ffmpeg-java/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java imagic_ffmpeg_java
python3 parsarium.py run ascii_pnm java imagic_ffmpeg_java controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java imagic_ffmpeg_java CORPUS_DIR runs/ascii_pnm-imagic_ffmpeg_java-replay
python3 parsarium.py afl build ascii_pnm java imagic_ffmpeg_java
python3 parsarium.py afl prepare ascii_pnm java imagic_ffmpeg_java runs/ascii_pnm-imagic_ffmpeg_java-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
