# @perseveranza-pets/milo — HTTP/1.1 / JavaScript

Pinned release: `0.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/perseveranza-pets-milo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript perseveranza_pets_milo
python3 parsarium.py run http11 javascript perseveranza_pets_milo controls/http11/request.http
python3 parsarium.py replay http11 javascript perseveranza_pets_milo CORPUS_DIR runs/http11-perseveranza_pets_milo-replay
python3 parsarium.py afl build http11 javascript perseveranza_pets_milo
python3 parsarium.py afl prepare http11 javascript perseveranza_pets_milo runs/http11-perseveranza_pets_milo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
