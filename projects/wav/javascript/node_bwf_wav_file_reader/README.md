# node-bwf-wav-file-reader — WAV / JavaScript

Pinned release: `1.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/node-bwf-wav-file-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript node_bwf_wav_file_reader
python3 parsarium.py run wav javascript node_bwf_wav_file_reader controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript node_bwf_wav_file_reader CORPUS_DIR runs/wav-node_bwf_wav_file_reader-replay
python3 parsarium.py afl build wav javascript node_bwf_wav_file_reader
python3 parsarium.py afl prepare wav javascript node_bwf_wav_file_reader runs/wav-node_bwf_wav_file_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
