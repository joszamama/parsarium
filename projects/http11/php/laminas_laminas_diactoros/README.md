# laminas/laminas-diactoros — HTTP/1.1 / PHP

Pinned release: `3.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/laminas-laminas-diactoros/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php laminas_laminas_diactoros
python3 parsarium.py run http11 php laminas_laminas_diactoros controls/http11/request.http
python3 parsarium.py replay http11 php laminas_laminas_diactoros CORPUS_DIR runs/http11-laminas_laminas_diactoros-replay
python3 parsarium.py afl build http11 php laminas_laminas_diactoros
python3 parsarium.py afl prepare http11 php laminas_laminas_diactoros runs/http11-laminas_laminas_diactoros-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
