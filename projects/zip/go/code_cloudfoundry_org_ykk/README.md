# code.cloudfoundry.org/ykk — ZIP / Go

Pinned release: `v0.0.0-20170424192843-e4df4ce2fd4d`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/code-cloudfoundry-org-ykk/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go code_cloudfoundry_org_ykk
python3 parsarium.py run zip go code_cloudfoundry_org_ykk controls/zip/hello.zip
python3 parsarium.py replay zip go code_cloudfoundry_org_ykk CORPUS_DIR runs/zip-code_cloudfoundry_org_ykk-replay
python3 parsarium.py afl build zip go code_cloudfoundry_org_ykk
python3 parsarium.py afl prepare zip go code_cloudfoundry_org_ykk runs/zip-code_cloudfoundry_org_ykk-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
