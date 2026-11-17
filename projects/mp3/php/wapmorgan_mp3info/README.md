# wapmorgan/mp3info — MP3 / PHP

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/wapmorgan-mp3info/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 php wapmorgan_mp3info
python3 parsarium.py run mp3 php wapmorgan_mp3info controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 php wapmorgan_mp3info CORPUS_DIR runs/mp3-wapmorgan_mp3info-replay
python3 parsarium.py afl build mp3 php wapmorgan_mp3info
python3 parsarium.py afl prepare mp3 php wapmorgan_mp3info runs/mp3-wapmorgan_mp3info-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** MPEG-1 Layer III CBR only. With the documented constructor and default settings ($framesCountRead = 2), Mp3Info reads the first frame header, jumps by a computed frame length to read a second header, estimates frames as ceil(audio bytes / frame length) and reports duration as (frames - 1) x 1152 / sample rate, so the MPEG-1 control's duration is one frame (0.02612 s) below the 11-frame oracle. It does not decode audio or walk every frame. On the MPEG-2 22.05 kHz stereo control it uses the MPEG-1 144-byte coefficient for frame length, skips the real third frame, and takes a false sync inside audio data at byte 236; it reports MPEG-2 Layer II, 24 kHz mono, 96 kbit/s and 3 frames. MPEG-2 and MPEG-2.5 are therefore not covered. VBR, Xing/Info, free-format, Layer I/II and tagged inputs are untested here; ID3v2 scope is the separate mp3_id3v2/php record.
