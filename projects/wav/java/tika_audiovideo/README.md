# tika-audiovideo — WAV / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/tika-audiovideo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java tika_audiovideo
python3 parsarium.py run wav java tika_audiovideo controls/wav/256-samples.wav
python3 parsarium.py replay wav java tika_audiovideo CORPUS_DIR runs/wav-tika_audiovideo-replay
python3 parsarium.py afl build wav java tika_audiovideo
python3 parsarium.py afl prepare wav java tika_audiovideo runs/wav-tika_audiovideo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
