# netty-codec-dns — DNS / Java

Pinned release: `4.2.21.Final`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/netty-codec-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java netty_codec_dns
python3 parsarium.py run dns java netty_codec_dns controls/dns/response.bin
python3 parsarium.py replay dns java netty_codec_dns CORPUS_DIR runs/dns-netty_codec_dns-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns java netty_codec_dns
python3 parsarium.py afl prepare dns java netty_codec_dns runs/dns-netty_codec_dns-afl --fandango 100
python3 parsarium.py afl run runs/dns-netty_codec_dns-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
