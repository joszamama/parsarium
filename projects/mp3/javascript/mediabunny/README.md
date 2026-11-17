# mediabunny — MP3 / JavaScript

Pinned release: `1.66.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/mediabunny/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript mediabunny
python3 parsarium.py run mp3 javascript mediabunny controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 javascript mediabunny CORPUS_DIR runs/mp3-mediabunny-replay
python3 parsarium.py afl build mp3 javascript mediabunny
python3 parsarium.py afl prepare mp3 javascript mediabunny runs/mp3-mediabunny-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only; two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support. mediabunny demuxes frames and reads headers; it does not decode MP3 audio without WebCodecs, which this path does not use.
