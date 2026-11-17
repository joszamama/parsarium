# simplejson — JSON / Python

Pinned release: `4.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control, result, and parser family](../../../../catalog/json/python/simplejson/README.md)

Run from the repository root:

```sh
python3 parsarium.py build json python simplejson
python3 parsarium.py run json python simplejson controls/json/structure.json
python3 parsarium.py replay json python simplejson CORPUS_DIR runs/json-simplejson-replay
python3 parsarium.py afl build json python simplejson
python3 parsarium.py afl prepare json python simplejson runs/json-simplejson-afl
```

`CORPUS_DIR` contains files to replay individually. The AFL++ prepare command writes a seeded run directory; it does not start a campaign.
