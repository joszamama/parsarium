# nicoverbruggen/mediaprobe — WAV / PHP

Pinned release: `v1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/nicoverbruggen-mediaprobe/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php nicoverbruggen_mediaprobe
python3 parsarium.py run wav php nicoverbruggen_mediaprobe controls/wav/256-samples.wav
python3 parsarium.py replay wav php nicoverbruggen_mediaprobe CORPUS_DIR runs/wav-nicoverbruggen_mediaprobe-replay
python3 parsarium.py afl build wav php nicoverbruggen_mediaprobe
python3 parsarium.py afl prepare wav php nicoverbruggen_mediaprobe runs/wav-nicoverbruggen_mediaprobe-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
