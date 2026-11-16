# phpmlkit/soundfile — WAV / PHP

Pinned release: `1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/phpmlkit-soundfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php phpmlkit_soundfile
python3 parsarium.py run wav php phpmlkit_soundfile controls/wav/256-samples.wav
python3 parsarium.py replay wav php phpmlkit_soundfile CORPUS_DIR runs/wav-phpmlkit_soundfile-replay
python3 parsarium.py afl build wav php phpmlkit_soundfile
python3 parsarium.py afl prepare wav php phpmlkit_soundfile runs/wav-phpmlkit_soundfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
