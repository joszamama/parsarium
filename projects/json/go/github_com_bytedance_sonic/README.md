# github.com/bytedance/sonic — JSON / Go

Pinned release: `v1.15.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control results, and parser family](../../../../catalog/json/go/github-com-bytedance-sonic/README.md)

On pinned Linux arm64 / Go 1.27.1, Sonic selects `UseSonicJSON`. Its Go `optdec` creates a DOM using a native NEON parser. Coverage and AFL++ feedback here include `optdec` Go blocks; the NEON assembly instructions are not line instrumented.

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_bytedance_sonic
python3 parsarium.py run json go github_com_bytedance_sonic controls/json/nested-object.json
python3 parsarium.py run json go github_com_bytedance_sonic controls/json/nested-array.json
python3 parsarium.py replay json go github_com_bytedance_sonic CORPUS_DIR runs/json-sonic-replay
python3 parsarium.py afl build json go github_com_bytedance_sonic
python3 parsarium.py afl prepare json go github_com_bytedance_sonic runs/json-sonic-afl
python3 projects/json/go/github_com_bytedance_sonic/verify-feedback.py
```

Replace `CORPUS_DIR` with a directory of JSON files. The AFL++ command prepares a seeded run; it does not start a campaign.
