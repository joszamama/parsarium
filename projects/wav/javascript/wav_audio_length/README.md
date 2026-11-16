# wav-audio-length — WAV / JavaScript

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/wav-audio-length/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript wav_audio_length
python3 parsarium.py run wav javascript wav_audio_length controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript wav_audio_length CORPUS_DIR runs/wav-wav_audio_length-replay
python3 parsarium.py afl build wav javascript wav_audio_length
python3 parsarium.py afl prepare wav javascript wav_audio_length runs/wav-wav_audio_length-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
