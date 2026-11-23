# pygame — WAV / Python

Pinned release: `2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/pygame/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python pygame
python3 parsarium.py run wav python pygame controls/wav/four-samples.wav
python3 parsarium.py replay wav python pygame CORPUS_DIR runs/wav-pygame-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav python pygame
python3 parsarium.py afl prepare wav python pygame runs/wav-pygame-afl --fandango 100
python3 parsarium.py afl run runs/wav-pygame-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Feedback scope:** AFL++ observes edges in the pinned `libSDL2_mixer-2-673d03d7.0.so.0.600.3` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
