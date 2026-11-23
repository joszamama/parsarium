# AudioSystem.getAudioFileFormat(File) — WAV / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/wav/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build wav java jdk_audiofileformat
python3 parsarium.py run wav java jdk_audiofileformat controls/wav/256-samples.wav
python3 parsarium.py replay wav java jdk_audiofileformat CORPUS_DIR runs/wav-jdk_audiofileformat-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav java jdk_audiofileformat
python3 parsarium.py afl prepare wav java jdk_audiofileformat runs/wav-jdk_audiofileformat-afl --fandango 100
python3 parsarium.py afl run runs/wav-jdk_audiofileformat-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
