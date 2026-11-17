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

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign. The reader and converter are selected directly from MP3SPI so the path does not depend on Java Sound provider discovery. The image includes JaCoCo source lines for MP3SPI and its soundlibs JLayer decoder as separate groups.

**Coverage limit:** Two valid untagged CBR Layer III controls. The provider shares JLayer decoder lineage with `javazoom:jlayer` and is a distinct public API path, not an independent decoder family.
