# jcodec — MP3 / Java

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/java/jcodec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 java jcodec
python3 parsarium.py run mp3 java jcodec controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 java jcodec CORPUS_DIR runs/mp3-jcodec-replay
python3 parsarium.py afl build mp3 java jcodec
python3 parsarium.py afl prepare mp3 java jcodec runs/mp3-jcodec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only; two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 or intensity-stereo support (Mp3Decoder throws on intensity stereo). jcodec is also counted under mp3_id3v2/java through the same MPEGAudioDemuxer; this path adds full Layer III decoding of untagged streams.
