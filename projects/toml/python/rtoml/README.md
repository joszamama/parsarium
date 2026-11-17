# rtoml — TOML / Python

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/python/rtoml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml python rtoml
python3 parsarium.py run toml python rtoml controls/toml/service-config.toml
python3 parsarium.py replay toml python rtoml CORPUS_DIR runs/toml-rtoml-replay
python3 parsarium.py afl build toml python rtoml
python3 parsarium.py afl prepare toml python rtoml runs/toml-rtoml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
