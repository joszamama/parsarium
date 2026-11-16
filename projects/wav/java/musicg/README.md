# musicg — WAV / Java

Pinned release: `1.4.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/musicg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java musicg
python3 parsarium.py run wav java musicg controls/wav/256-samples.wav
python3 parsarium.py replay wav java musicg CORPUS_DIR runs/wav-musicg-replay
python3 parsarium.py afl build wav java musicg
python3 parsarium.py afl prepare wav java musicg runs/wav-musicg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
