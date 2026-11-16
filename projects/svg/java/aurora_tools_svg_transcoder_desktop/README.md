# aurora-tools-svg-transcoder-desktop — SVG / Java

Pinned release: `1.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/aurora-tools-svg-transcoder-desktop/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java aurora_tools_svg_transcoder_desktop
python3 parsarium.py run svg java aurora_tools_svg_transcoder_desktop controls/svg/red-green.svg
python3 parsarium.py replay svg java aurora_tools_svg_transcoder_desktop CORPUS_DIR runs/svg-aurora_tools_svg_transcoder_desktop-replay
python3 parsarium.py afl build svg java aurora_tools_svg_transcoder_desktop
python3 parsarium.py afl prepare svg java aurora_tools_svg_transcoder_desktop runs/svg-aurora_tools_svg_transcoder_desktop-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
