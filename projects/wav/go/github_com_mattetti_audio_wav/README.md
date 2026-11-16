# github.com/mattetti/audio/wav — WAV / Go

Pinned release: `v0.0.0-20240411020228-c5379f9b5b61`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/go/github-com-mattetti-audio-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav go github_com_mattetti_audio_wav
python3 parsarium.py run wav go github_com_mattetti_audio_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav go github_com_mattetti_audio_wav CORPUS_DIR runs/wav-github_com_mattetti_audio_wav-replay
python3 parsarium.py afl build wav go github_com_mattetti_audio_wav
python3 parsarium.py afl prepare wav go github_com_mattetti_audio_wav runs/wav-github_com_mattetti_audio_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
