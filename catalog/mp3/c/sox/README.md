# sox — MP3 / C

- **Pinned release:** `14.4.2`
- **Upstream:** [source repository](<https://sourceforge.net/projects/sox/>) · [Debian](<https://tracker.debian.org/pkg/sox>)
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** MP3 audio parsing and one decoded sample from a valid ID3v2-tagged input; ID3v2 text is not exposed
- **Underlying family:** libsox MP3 handler over libmad decoder
- **Local input API:** `sox_init; sox_open_read(local filename, NULL, NULL, NULL); sox_read decoded sample; filetype and signal fields`
- **Documentation:** [API reference](<https://sourceforge.net/p/sox/code/ci/master/tree/src/example0.c>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3/parsers.json) · [control verification](../../../../data/c/mp3/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "filetype": "mp3",
  "sample_rate": 8000,
  "channels": 1,
  "decoded_samples": 1
}
```

The pinned src/mp3.c is the MP3 format handler and the installed libsox links libmad. C and C++ call sites use the same C library. The valid ID3v2-tagged control is accepted, but libsox does not return its title.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/c/sox/README.md)

```sh
python3 parsarium.py build mp3 c sox
python3 parsarium.py run mp3 c sox controls/mp3/id3v2-tagged-tone.mp3
```
