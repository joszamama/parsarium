# JLayer — MP3 / Java

Pinned open-source release: `javazoom:jlayer:1.0.1` (LGPL-2.0-or-later from source headers). [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json)

`Bitstream` reads from a local `InputStream` and parses each frame header. `Decoder.decodeFrame` runs the pure-Java Layer III decoder. The adapter reports stream format and decoded sample count across every frame. The two untagged valid CBR controls match the independent header oracle exactly; no ID3, VBR or malformed-input behavior is inferred.

## Run from the repository root

```sh
python3 parsarium.py build mp3 java jlayer
python3 parsarium.py run mp3 java jlayer controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 java jlayer CORPUS_DIR runs/mp3-jlayer-replay
python3 parsarium.py afl build mp3 java jlayer
python3 parsarium.py afl prepare mp3 java jlayer runs/mp3-jlayer-afl
python3 parsarium.py afl run runs/mp3-jlayer-afl --check
```

`CORPUS_DIR` is a directory of user-provided inputs. Preparing AFL++ and running `--check` only validate the launcher and control path; they do not start a fuzz campaign. JaCoCo source lines and the AFL++ parser-line bridge cover JLayer's own `Bitstream`, `Header` and `LayerIIIDecoder` code. The bridge receipt and fixed second-control differential are in [the AFL overlay](../../../../fuzzing/afl-native/mp3/java/jlayer/verification.json) and [the differential receipt](../../../../data/java/mp3/jlayer-feedback-differential.json).
