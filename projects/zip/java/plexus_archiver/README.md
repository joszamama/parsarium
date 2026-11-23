# plexus-archiver — ZIP / Java

Pinned release: `4.15.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/plexus-archiver/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java plexus_archiver
python3 parsarium.py run zip java plexus_archiver controls/zip/hello.zip
python3 parsarium.py replay zip java plexus_archiver CORPUS_DIR runs/zip-plexus_archiver-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip java plexus_archiver
python3 parsarium.py afl prepare zip java plexus_archiver runs/zip-plexus_archiver-afl --fandango 100
python3 parsarium.py afl run runs/zip-plexus_archiver-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
