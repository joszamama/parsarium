# github.com/hajimehoshi/go-mp3 — MP3 / Go

Pinned release: `v0.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-hajimehoshi-go-mp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_hajimehoshi_go_mp3
python3 parsarium.py run mp3 go github_com_hajimehoshi_go_mp3 controls/mp3/id3v2-tagged-tone-44k.mp3
python3 parsarium.py replay mp3 go github_com_hajimehoshi_go_mp3 CORPUS_DIR runs/mp3-github_com_hajimehoshi_go_mp3-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp3 go github_com_hajimehoshi_go_mp3
python3 parsarium.py afl prepare mp3 go github_com_hajimehoshi_go_mp3 runs/mp3-github_com_hajimehoshi_go_mp3-afl --fandango 100
python3 parsarium.py afl run runs/mp3-github_com_hajimehoshi_go_mp3-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
