# owen-oj/laravel-getid3 — WAV / PHP

Pinned release: `v2.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/owen-oj-laravel-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php owen_oj_laravel_getid3
python3 parsarium.py run wav php owen_oj_laravel_getid3 controls/wav/256-samples.wav
python3 parsarium.py replay wav php owen_oj_laravel_getid3 CORPUS_DIR runs/wav-owen_oj_laravel_getid3-replay
python3 parsarium.py afl build wav php owen_oj_laravel_getid3
python3 parsarium.py afl prepare wav php owen_oj_laravel_getid3 runs/wav-owen_oj_laravel_getid3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
