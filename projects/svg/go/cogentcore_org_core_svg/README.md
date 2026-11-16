# cogentcore.org/core/svg — SVG / Go

Pinned release: `v0.5.30`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/cogentcore-org-core-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go cogentcore_org_core_svg
python3 parsarium.py run svg go cogentcore_org_core_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go cogentcore_org_core_svg CORPUS_DIR runs/svg-cogentcore_org_core_svg-replay
python3 parsarium.py afl build svg go cogentcore_org_core_svg
python3 parsarium.py afl prepare svg go cogentcore_org_core_svg runs/svg-cogentcore_org_core_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
