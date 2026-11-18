# github.com/mateusz834/dnsmsg — DNS / Go

Pinned release: `v0.0.0-20231225175121-c6b857669b66`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/github-com-mateusz834-dnsmsg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go github_com_mateusz834_dnsmsg
python3 parsarium.py run dns go github_com_mateusz834_dnsmsg controls/dns/response.bin
python3 parsarium.py replay dns go github_com_mateusz834_dnsmsg CORPUS_DIR runs/dns-github_com_mateusz834_dnsmsg-replay
python3 parsarium.py afl build dns go github_com_mateusz834_dnsmsg
python3 parsarium.py afl prepare dns go github_com_mateusz834_dnsmsg runs/dns-github_com_mateusz834_dnsmsg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
