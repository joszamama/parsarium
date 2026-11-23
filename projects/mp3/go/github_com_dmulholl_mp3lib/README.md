# github.com/dmulholl/mp3lib — MP3 / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-dmulholl-mp3lib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py run mp3 go github_com_dmulholl_mp3lib controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 go github_com_dmulholl_mp3lib CORPUS_DIR runs/mp3-github_com_dmulholl_mp3lib-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py afl prepare mp3 go github_com_dmulholl_mp3lib runs/mp3-github_com_dmulholl_mp3lib-afl --fandango 100
python3 parsarium.py afl run runs/mp3-github_com_dmulholl_mp3lib-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Frame parser only; does not decode PCM. Two untagged CBR controls do not establish VBR or complete MPEG audio support.
