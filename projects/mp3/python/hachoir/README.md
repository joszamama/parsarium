# hachoir — MP3 / Python

Pinned release: `3.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/hachoir/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 python hachoir
python3 parsarium.py run mp3 python hachoir controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 python hachoir CORPUS_DIR runs/mp3-hachoir-replay
python3 parsarium.py afl build mp3 python hachoir
python3 parsarium.py afl prepare mp3 python hachoir runs/mp3-hachoir-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only. The harness selects hachoir's MpegAudioFile parser directly (no guessParser dispatch) with validate=True, iterates every frame[] field set to the end of the input, and accepts only streams made entirely of complete Layer III frames with one header tuple: no leading padding, trailing raw bytes, truncated final frame or ID3 tags. It reports MPEG version, layer, sample rate, bitrate, channel mode, channels and the walked frame count; it reads 32-bit frame headers and frame lengths and does not decode audio or side information. Two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 or tagged-file support.
