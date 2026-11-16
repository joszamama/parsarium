# get-audio-duration — WAV / JavaScript

Pinned release: `4.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/get-audio-duration/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript get_audio_duration
python3 parsarium.py run wav javascript get_audio_duration controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript get_audio_duration CORPUS_DIR runs/wav-get_audio_duration-replay
python3 parsarium.py afl build wav javascript get_audio_duration
python3 parsarium.py afl prepare wav javascript get_audio_duration runs/wav-get_audio_duration-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
