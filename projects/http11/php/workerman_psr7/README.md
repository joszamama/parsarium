# workerman/psr7 — HTTP/1.1 / PHP

Pinned release: `v2.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/workerman-psr7/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php workerman_psr7
python3 parsarium.py run http11 php workerman_psr7 controls/http11/request.http
python3 parsarium.py replay http11 php workerman_psr7 CORPUS_DIR runs/http11-workerman_psr7-replay
python3 parsarium.py afl build http11 php workerman_psr7
python3 parsarium.py afl prepare http11 php workerman_psr7 runs/http11-workerman_psr7-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
