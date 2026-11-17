# jlayer — MP3 / Java

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/java/jlayer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 java jlayer
python3 parsarium.py run mp3 java jlayer controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 java jlayer CORPUS_DIR runs/mp3-jlayer-replay
python3 parsarium.py afl build mp3 java jlayer
python3 parsarium.py afl prepare mp3 java jlayer runs/mp3-jlayer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III controls only; two valid CBR streams do not establish VBR, Xing/Info, free-format, Layer I/II or MPEG-2.5 behavior. Same original JLayer lineage as soundlibs and libGDX forks, but independent of JCodec.
