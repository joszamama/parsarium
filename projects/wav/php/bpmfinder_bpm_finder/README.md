# bpmfinder/bpm-finder — WAV / PHP

Pinned release: `v0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/bpmfinder-bpm-finder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php bpmfinder_bpm_finder
python3 parsarium.py run wav php bpmfinder_bpm_finder controls/wav/120-bpm-clicks.wav
python3 parsarium.py replay wav php bpmfinder_bpm_finder CORPUS_DIR runs/wav-bpmfinder_bpm_finder-replay
python3 parsarium.py afl build wav php bpmfinder_bpm_finder
python3 parsarium.py afl prepare wav php bpmfinder_bpm_finder runs/wav-bpmfinder_bpm_finder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
