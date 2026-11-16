# workerman/workerman — HTTP/1.1 / PHP

Pinned release: `v5.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/workerman-workerman/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php workerman_workerman
python3 parsarium.py run http11 php workerman_workerman controls/http11/request.http
python3 parsarium.py replay http11 php workerman_workerman CORPUS_DIR runs/http11-workerman_workerman-replay
python3 parsarium.py afl build http11 php workerman_workerman
python3 parsarium.py afl prepare http11 php workerman_workerman runs/http11-workerman_workerman-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
