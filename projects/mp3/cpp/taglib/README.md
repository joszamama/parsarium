# taglib — MP3 / C++

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/cpp/taglib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 cpp taglib
python3 parsarium.py run mp3 cpp taglib controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 cpp taglib CORPUS_DIR runs/mp3-taglib-replay
python3 parsarium.py afl build mp3 cpp taglib
python3 parsarium.py afl prepare mp3 cpp taglib runs/mp3-taglib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only. TagLib parses frame headers (and Xing/VBRI when present) to report audio properties; it does not decode Layer III audio, so main data, Huffman and synthesis are not exercised. For CBR streams without a Xing/VBRI header the length is derived from stream size and the first frame's bitrate. Two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support. TagLib is also counted under mp3_id3v2/cpp for ID3v2 scope; this path is the plain-frame property scope.
