# maximal/audio-waveform — WAV / PHP

Pinned release: `1.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/maximal-audio-waveform/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php maximal_audio_waveform
python3 parsarium.py run wav php maximal_audio_waveform controls/wav/256-samples.wav
python3 parsarium.py replay wav php maximal_audio_waveform CORPUS_DIR runs/wav-maximal_audio_waveform-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav php maximal_audio_waveform
python3 parsarium.py afl prepare wav php maximal_audio_waveform runs/wav-maximal_audio_waveform-afl --fandango 100
python3 parsarium.py afl run runs/wav-maximal_audio_waveform-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
