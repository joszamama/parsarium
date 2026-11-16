# aubio — WAV / C++

Pinned release: `0.4.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/aubio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp aubio
python3 parsarium.py run wav cpp aubio controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp aubio CORPUS_DIR runs/wav-aubio-replay
python3 parsarium.py afl build wav cpp aubio
python3 parsarium.py afl prepare wav cpp aubio runs/wav-aubio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
