# tangled.sh/seiso.moe/magna — DNS / Go

Pinned release: `v0.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/tangled-sh-seiso-moe-magna/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go tangled_sh_seiso_moe_magna
python3 parsarium.py run dns go tangled_sh_seiso_moe_magna controls/dns/response.bin
python3 parsarium.py replay dns go tangled_sh_seiso_moe_magna CORPUS_DIR runs/dns-tangled_sh_seiso_moe_magna-replay
python3 parsarium.py afl build dns go tangled_sh_seiso_moe_magna
python3 parsarium.py afl prepare dns go tangled_sh_seiso_moe_magna runs/dns-tangled_sh_seiso_moe_magna-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
