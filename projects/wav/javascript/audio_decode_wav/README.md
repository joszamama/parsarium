# @audio/decode-wav — WAV / JavaScript

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/audio-decode-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript audio_decode_wav
python3 parsarium.py run wav javascript audio_decode_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript audio_decode_wav CORPUS_DIR runs/wav-audio_decode_wav-replay
python3 parsarium.py afl build wav javascript audio_decode_wav
python3 parsarium.py afl prepare wav javascript audio_decode_wav runs/wav-audio_decode_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
