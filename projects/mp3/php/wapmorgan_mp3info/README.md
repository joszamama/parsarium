# wapmorgan/mp3info — MP3 / PHP

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Cell ranking, control results, and parser family](../../../../data/php/mp3/ranking.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 php wapmorgan_mp3info
python3 parsarium.py run mp3 php wapmorgan_mp3info controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 php wapmorgan_mp3info CORPUS_DIR runs/mp3-wapmorgan_mp3info-replay
python3 parsarium.py afl build mp3 php wapmorgan_mp3info
python3 parsarium.py afl prepare mp3 php wapmorgan_mp3info runs/mp3-wapmorgan_mp3info-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** MPEG-1 Layer III CBR only. Mp3Info reads two frame headers, estimates frames from audio bytes and the computed frame length, and reports duration as (frames - 1) × 1152 / sample rate, one frame below the 11-frame oracle on the MPEG-1 control. It does not decode audio. On the MPEG-2 22.05 kHz stereo control it reads a false sync at byte 236 and reports Layer II, 24 kHz mono, 96 kbit/s and 3 frames, so MPEG-2 and MPEG-2.5 are not covered. VBR, Xing/Info, free-format, Layer I/II and tagged inputs are untested; ID3v2 scope is the separate mp3_id3v2/php record.
