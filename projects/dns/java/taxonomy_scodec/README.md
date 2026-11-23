# taxonomy-scodec_2.13 — DNS / Java

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/taxonomy-scodec-2-13/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java taxonomy_scodec
python3 parsarium.py run dns java taxonomy_scodec controls/dns/response.bin
python3 parsarium.py replay dns java taxonomy_scodec CORPUS_DIR runs/dns-taxonomy_scodec-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns java taxonomy_scodec
python3 parsarium.py afl prepare dns java taxonomy_scodec runs/dns-taxonomy_scodec-afl --fandango 100
python3 parsarium.py afl run runs/dns-taxonomy_scodec-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
