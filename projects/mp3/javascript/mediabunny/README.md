# mediabunny — MP3 / JavaScript

Pinned release: `1.66.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

Untagged MPEG Layer III frames reach mediabunny's own MP3 demuxer through `Input` with a `BufferSource`. The harness counts frames as encoded packets and reads sample rate, channel count and duration from the track; it does not decode audio.

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript mediabunny
python3 parsarium.py run mp3 javascript mediabunny controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 javascript mediabunny CORPUS_DIR runs/mp3-mediabunny-replay
python3 parsarium.py afl build mp3 javascript mediabunny
python3 parsarium.py afl prepare mp3 javascript mediabunny runs/mp3-mediabunny-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
