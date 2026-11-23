# tika-audiovideo — WAV / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/tika-audiovideo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java tika_audiovideo
python3 parsarium.py run wav java tika_audiovideo controls/wav/256-samples.wav
python3 parsarium.py replay wav java tika_audiovideo CORPUS_DIR runs/wav-tika_audiovideo-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav java tika_audiovideo
python3 parsarium.py afl prepare wav java tika_audiovideo runs/wav-tika_audiovideo-afl --fandango 100
python3 parsarium.py afl run runs/wav-tika_audiovideo-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
