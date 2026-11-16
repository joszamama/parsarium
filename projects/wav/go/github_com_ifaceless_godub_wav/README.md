# github.com/iFaceless/godub/wav — WAV / Go

Pinned release: `v0.0.0-20200728093528-a30bb4d1a0f1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/go/github-com-ifaceless-godub-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav go github_com_ifaceless_godub_wav
python3 parsarium.py run wav go github_com_ifaceless_godub_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav go github_com_ifaceless_godub_wav CORPUS_DIR runs/wav-github_com_ifaceless_godub_wav-replay
python3 parsarium.py afl build wav go github_com_ifaceless_godub_wav
python3 parsarium.py afl prepare wav go github_com_ifaceless_godub_wav runs/wav-github_com_ifaceless_godub_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
