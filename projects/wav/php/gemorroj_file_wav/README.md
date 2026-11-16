# gemorroj/file-wav — WAV / PHP

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/gemorroj-file-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php gemorroj_file_wav
python3 parsarium.py run wav php gemorroj_file_wav controls/wav/256-samples.wav
python3 parsarium.py replay wav php gemorroj_file_wav CORPUS_DIR runs/wav-gemorroj_file_wav-replay
python3 parsarium.py afl build wav php gemorroj_file_wav
python3 parsarium.py afl prepare wav php gemorroj_file_wav runs/wav-gemorroj_file_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
