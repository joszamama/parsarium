# mp3spi — MP3 / Java

Pinned release: `1.9.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/java/mp3spi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 java mp3spi
python3 parsarium.py run mp3 java mp3spi controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 java mp3spi CORPUS_DIR runs/mp3-mp3spi-replay
python3 parsarium.py afl build mp3 java mp3spi
python3 parsarium.py afl prepare mp3 java mp3spi runs/mp3-mp3spi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two untagged CBR MPEG Layer III controls. MP3SPI uses Java Sound SPI but the adapter selects its reader and converter directly; PCM decoding delegates to the soundlibs JLayer fork, the same decoder lineage as javazoom:jlayer. VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 and ID3 are outside these checks.
