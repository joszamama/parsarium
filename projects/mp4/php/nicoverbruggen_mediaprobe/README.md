# nicoverbruggen/mediaprobe — MP4 / PHP

Pinned release: `v1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/nicoverbruggen-mediaprobe/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php nicoverbruggen_mediaprobe
python3 parsarium.py run mp4 php nicoverbruggen_mediaprobe controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php nicoverbruggen_mediaprobe CORPUS_DIR runs/mp4-nicoverbruggen_mediaprobe-replay
python3 parsarium.py afl build mp4 php nicoverbruggen_mediaprobe
python3 parsarium.py afl prepare mp4 php nicoverbruggen_mediaprobe runs/mp4-nicoverbruggen_mediaprobe-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
