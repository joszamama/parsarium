# allegro — WAV / C++

Pinned release: `5.2.11.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/allegro/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp allegro
python3 parsarium.py run wav cpp allegro controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp allegro CORPUS_DIR runs/wav-allegro-replay
python3 parsarium.py afl build wav cpp allegro
python3 parsarium.py afl prepare wav cpp allegro runs/wav-allegro-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
