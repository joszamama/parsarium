# github.com/andrianbdn/iospng — PNG / Go

Pinned release: `v0.0.0-20180730113000-dccef1992541`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-andrianbdn-iospng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_andrianbdn_iospng
python3 parsarium.py run png go github_com_andrianbdn_iospng controls/png/red-green.png
python3 parsarium.py replay png go github_com_andrianbdn_iospng CORPUS_DIR runs/png-github_com_andrianbdn_iospng-replay
python3 parsarium.py afl build png go github_com_andrianbdn_iospng
python3 parsarium.py afl prepare png go github_com_andrianbdn_iospng runs/png-github_com_andrianbdn_iospng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
