# github.com/shadowy-pycoder/mshark/layers — DNS / Go

Pinned release: `v0.0.32`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/github-com-shadowy-pycoder-mshark-layers/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go github_com_shadowy_pycoder_mshark_layers
python3 parsarium.py run dns go github_com_shadowy_pycoder_mshark_layers controls/dns/response.bin
python3 parsarium.py replay dns go github_com_shadowy_pycoder_mshark_layers CORPUS_DIR runs/dns-github_com_shadowy_pycoder_mshark_layers-replay
python3 parsarium.py afl build dns go github_com_shadowy_pycoder_mshark_layers
python3 parsarium.py afl prepare dns go github_com_shadowy_pycoder_mshark_layers runs/dns-github_com_shadowy_pycoder_mshark_layers-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
