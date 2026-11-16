# github.com/xigh/go-wavreader — WAV / Go

Pinned release: `v0.0.0-20210516212152-f49019aa7352`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/go/github-com-xigh-go-wavreader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav go github_com_xigh_go_wavreader
python3 parsarium.py run wav go github_com_xigh_go_wavreader controls/wav/four-samples.wav
python3 parsarium.py replay wav go github_com_xigh_go_wavreader CORPUS_DIR runs/wav-github_com_xigh_go_wavreader-replay
python3 parsarium.py afl build wav go github_com_xigh_go_wavreader
python3 parsarium.py afl prepare wav go github_com_xigh_go_wavreader runs/wav-github_com_xigh_go_wavreader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
