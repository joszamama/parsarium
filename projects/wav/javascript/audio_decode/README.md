# audio-decode — WAV / JavaScript

Pinned release: `3.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/audio-decode-774b86ab/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript audio_decode
python3 parsarium.py run wav javascript audio_decode controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript audio_decode CORPUS_DIR runs/wav-audio_decode-replay
python3 parsarium.py afl build wav javascript audio_decode
python3 parsarium.py afl prepare wav javascript audio_decode runs/wav-audio_decode-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
