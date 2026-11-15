# github.com/klauspost/compress/zip — ZIP / Go

Pinned release: `v1.20.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-klauspost-compress-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go klauspost_compress_zip
python3 parsarium.py run zip go klauspost_compress_zip controls/zip/hello.zip
python3 parsarium.py replay zip go klauspost_compress_zip CORPUS_DIR runs/zip-klauspost_compress_zip-replay
python3 parsarium.py afl build zip go klauspost_compress_zip
python3 parsarium.py afl prepare zip go klauspost_compress_zip runs/zip-klauspost_compress_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
