# toml-java — TOML / Java

Pinned release: `13.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/java/toml-java/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml java vieiro_toml_java
python3 parsarium.py run toml java vieiro_toml_java controls/toml/service-config.toml
python3 parsarium.py replay toml java vieiro_toml_java CORPUS_DIR runs/toml-vieiro_toml_java-replay
python3 parsarium.py afl build toml java vieiro_toml_java
python3 parsarium.py afl prepare toml java vieiro_toml_java runs/toml-vieiro_toml_java-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
