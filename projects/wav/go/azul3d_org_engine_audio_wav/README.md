# azul3d.org/engine/audio/wav — WAV / Go

Pinned release: `v0.0.0-20211024043305-793ea6c2839d`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/go/azul3d-org-engine-audio-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav go azul3d_org_engine_audio_wav
python3 parsarium.py run wav go azul3d_org_engine_audio_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav go azul3d_org_engine_audio_wav CORPUS_DIR runs/wav-azul3d_org_engine_audio_wav-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav go azul3d_org_engine_audio_wav
python3 parsarium.py afl prepare wav go azul3d_org_engine_audio_wav runs/wav-azul3d_org_engine_audio_wav-afl --fandango 100
python3 parsarium.py afl run runs/wav-azul3d_org_engine_audio_wav-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
