# owen-oj/laravel-getid3 — MP4 / PHP

Pinned release: `v2.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/owen-oj-laravel-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php owen_oj_laravel_getid3
python3 parsarium.py run mp4 php owen_oj_laravel_getid3 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php owen_oj_laravel_getid3 CORPUS_DIR runs/mp4-owen_oj_laravel_getid3-replay
python3 parsarium.py afl build mp4 php owen_oj_laravel_getid3
python3 parsarium.py afl prepare mp4 php owen_oj_laravel_getid3 runs/mp4-owen_oj_laravel_getid3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
