# @uttori/audio-wave — WAV / JavaScript

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/uttori-audio-wave/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript uttori_audio_wave
python3 parsarium.py run wav javascript uttori_audio_wave controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript uttori_audio_wave CORPUS_DIR runs/wav-uttori_audio_wave-replay
python3 parsarium.py afl build wav javascript uttori_audio_wave
python3 parsarium.py afl prepare wav javascript uttori_audio_wave runs/wav-uttori_audio_wave-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
