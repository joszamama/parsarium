# github.com/moutend/go-wav — WAV / Go

Pinned release: `v0.0.0-20170820031854-56127fbbb7ba`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/go/github-com-moutend-go-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav go github_com_moutend_go_wav
python3 parsarium.py run wav go github_com_moutend_go_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav go github_com_moutend_go_wav CORPUS_DIR runs/wav-github_com_moutend_go_wav-replay
python3 parsarium.py afl build wav go github_com_moutend_go_wav
python3 parsarium.py afl prepare wav go github_com_moutend_go_wav runs/wav-github_com_moutend_go_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
