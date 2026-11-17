# tinytag — MP3 / Python

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/tinytag/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 python tinytag
python3 parsarium.py run mp3 python tinytag controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 python tinytag CORPUS_DIR runs/mp3-tinytag-replay
python3 parsarium.py afl build mp3 python tinytag
python3 parsarium.py afl prepare mp3 python tinytag runs/mp3-tinytag-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only. TinyTag picks its _MPEG reader from the frame sync at byte 0, walks frame headers, and for a stream without Xing/Info/VBRI stops after five equal-bitrate frames and estimates duration from stream size divided by their mean frame length. It reports sample rate, channels, bitrate and duration, not MPEG version, layer or frame count. It does not decode audio. The two full-length CBR controls run the same TinyTag lines; parser feedback differs only for a valid three-frame prefix that ends before CBR detection. Two valid CBR controls do not establish VBR, free-format, Layer I/II, or MPEG-2.5 support.
