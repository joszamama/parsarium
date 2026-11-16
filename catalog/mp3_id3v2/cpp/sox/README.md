# sox — MP3 with ID3v2 / C++

- **Pinned release:** `14.4.2`
- **License:** GPL-2.0-or-later AND LGPL-2.1-or-later
- **Parsed scope:** MP3 audio parsing and one decoded sample from a valid ID3v2-tagged input; ID3v2 text is not exposed
- **Underlying family:** libsox MP3 handler over libmad decoder
- **Local input API:** `sox_init; sox_open_read(local filename, NULL, NULL, NULL); sox_read decoded sample; filetype and signal fields`
- **Documentation:** [API reference](<https://sourceforge.net/p/sox/code/ci/master/tree/src/example0.c>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/cpp/sox/README.md)

```sh
python3 parsarium.py build mp3_id3v2 cpp sox
python3 parsarium.py run mp3_id3v2 cpp sox controls/mp3_id3v2/tone-tags.mp3
```
