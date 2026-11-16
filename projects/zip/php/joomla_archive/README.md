# joomla/archive — ZIP / PHP

Pinned release: `4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/joomla-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php joomla_archive
python3 parsarium.py run zip php joomla_archive controls/zip/hello.zip
python3 parsarium.py replay zip php joomla_archive CORPUS_DIR runs/zip-joomla_archive-replay
python3 parsarium.py afl build zip php joomla_archive
python3 parsarium.py afl prepare zip php joomla_archive runs/zip-joomla_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
