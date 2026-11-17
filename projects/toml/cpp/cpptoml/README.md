# cpptoml — TOML / C++

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/cpp/cpptoml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml cpp cpptoml
python3 parsarium.py run toml cpp cpptoml controls/toml/service-config.toml
python3 parsarium.py replay toml cpp cpptoml CORPUS_DIR runs/toml-cpptoml-replay
python3 parsarium.py afl build toml cpp cpptoml
python3 parsarium.py afl prepare toml cpp cpptoml runs/toml-cpptoml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
