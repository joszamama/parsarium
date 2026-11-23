# netty — HTTP/1.1 / Java

Pinned release: `3.10.6.Final`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/netty/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java netty
python3 parsarium.py run http11 java netty controls/http11/request.http
python3 parsarium.py replay http11 java netty CORPUS_DIR runs/http11-netty-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build http11 java netty
python3 parsarium.py afl prepare http11 java netty runs/http11-netty-afl --fandango 100
python3 parsarium.py afl run runs/http11-netty-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
