# pygame — WAV / Python

Pinned release: `2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/pygame/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python pygame
python3 parsarium.py run wav python pygame controls/wav/four-samples.wav
python3 parsarium.py replay wav python pygame CORPUS_DIR runs/wav-pygame-replay
python3 parsarium.py afl build wav python pygame
python3 parsarium.py afl prepare wav python pygame runs/wav-pygame-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Feedback scope:** AFL++ observes edges in the pinned `libSDL2_mixer-2-673d03d7.0.so.0.600.3` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
