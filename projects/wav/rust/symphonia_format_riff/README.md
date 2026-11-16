# symphonia-format-riff — WAV / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/symphonia-format-riff/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust symphonia_format_riff
python3 parsarium.py run wav rust symphonia_format_riff controls/wav/four-samples.wav
python3 parsarium.py replay wav rust symphonia_format_riff CORPUS_DIR runs/wav-symphonia_format_riff-replay
python3 parsarium.py afl build wav rust symphonia_format_riff
python3 parsarium.py afl prepare wav rust symphonia_format_riff runs/wav-symphonia_format_riff-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
