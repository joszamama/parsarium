# audiostreamify/hvap — WAV / PHP

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/audiostreamify-hvap/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php audiostreamify_hvap
python3 parsarium.py run wav php audiostreamify_hvap controls/wav/256-samples.wav
python3 parsarium.py replay wav php audiostreamify_hvap CORPUS_DIR runs/wav-audiostreamify_hvap-replay
python3 parsarium.py afl build wav php audiostreamify_hvap
python3 parsarium.py afl prepare wav php audiostreamify_hvap runs/wav-audiostreamify_hvap-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
