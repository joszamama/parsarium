# gitee.com/shiqiyue/go-vips — ASCII PNM / Go

Pinned release: `v0.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/gitee-com-shiqiyue-go-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go gitee_com_shiqiyue_go_vips
python3 parsarium.py run ascii_pnm go gitee_com_shiqiyue_go_vips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go gitee_com_shiqiyue_go_vips CORPUS_DIR runs/ascii_pnm-gitee_com_shiqiyue_go_vips-replay
python3 parsarium.py afl build ascii_pnm go gitee_com_shiqiyue_go_vips
python3 parsarium.py afl prepare ascii_pnm go gitee_com_shiqiyue_go_vips runs/ascii_pnm-gitee_com_shiqiyue_go_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
