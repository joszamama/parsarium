# @audio/decode — WAV / JavaScript

Pinned release: `4.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/audio-decode-979380cb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript scoped_audio_decode
python3 parsarium.py run wav javascript scoped_audio_decode controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript scoped_audio_decode CORPUS_DIR runs/wav-scoped_audio_decode-replay
python3 parsarium.py afl build wav javascript scoped_audio_decode
python3 parsarium.py afl prepare wav javascript scoped_audio_decode runs/wav-scoped_audio_decode-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
