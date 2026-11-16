# github.com/gopxl/beep/v2/wav — WAV / Go

Pinned release: `v2.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/go/github-com-gopxl-beep-v2-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav go github_com_gopxl_beep_v2_wav
python3 parsarium.py run wav go github_com_gopxl_beep_v2_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav go github_com_gopxl_beep_v2_wav CORPUS_DIR runs/wav-github_com_gopxl_beep_v2_wav-replay
python3 parsarium.py afl build wav go github_com_gopxl_beep_v2_wav
python3 parsarium.py afl prepare wav go github_com_gopxl_beep_v2_wav runs/wav-github_com_gopxl_beep_v2_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
