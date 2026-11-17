# mp3spi — MP3 / Java

Pinned release: `1.9.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/java/mp3spi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 java mp3spi
python3 parsarium.py run mp3_id3v2 java mp3spi controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 java mp3spi CORPUS_DIR runs/mp3_id3v2-mp3spi-replay
python3 parsarium.py afl build mp3_id3v2 java mp3spi
python3 parsarium.py afl prepare mp3_id3v2 java mp3spi runs/mp3_id3v2-mp3spi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
