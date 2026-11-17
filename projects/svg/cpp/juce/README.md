# juce — SVG / C++

Pinned release: `9.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/juce/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp juce
python3 parsarium.py run svg cpp juce controls/svg/red-green.svg
python3 parsarium.py replay svg cpp juce CORPUS_DIR runs/svg-juce-replay
python3 parsarium.py afl build svg cpp juce
python3 parsarium.py afl prepare svg cpp juce runs/svg-juce-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
