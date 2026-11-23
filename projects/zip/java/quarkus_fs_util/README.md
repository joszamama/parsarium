# quarkus-fs-util — ZIP / Java

Pinned release: `1.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/quarkus-fs-util/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java quarkus_fs_util
python3 parsarium.py run zip java quarkus_fs_util controls/zip/hello.zip
python3 parsarium.py replay zip java quarkus_fs_util CORPUS_DIR runs/zip-quarkus_fs_util-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip java quarkus_fs_util
python3 parsarium.py afl prepare zip java quarkus_fs_util runs/zip-quarkus_fs_util-afl --fandango 100
python3 parsarium.py afl run runs/zip-quarkus_fs_util-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
