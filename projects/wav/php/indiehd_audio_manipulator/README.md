# indiehd/audio-manipulator — WAV / PHP

Pinned release: `v4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/indiehd-audio-manipulator/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php indiehd_audio_manipulator
python3 parsarium.py run wav php indiehd_audio_manipulator controls/wav/256-samples.wav
python3 parsarium.py replay wav php indiehd_audio_manipulator CORPUS_DIR runs/wav-indiehd_audio_manipulator-replay
python3 parsarium.py afl build wav php indiehd_audio_manipulator
python3 parsarium.py afl prepare wav php indiehd_audio_manipulator runs/wav-indiehd_audio_manipulator-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
