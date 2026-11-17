# Go XML wrapper gates — lead probes

This is a reproducible **unselected lead probe**, not a Parsarium parser project. It runs five Go XML leads (goxml2json, VictorLowther/simplexml/dom, subchen/go-xmldom, sbabiv/xml2map, dgrr/quickxml) on the two valid XML controls inside the pinned Go 1.27.1 image, with Go coverage limited to each lead's own package.

From the repository root:

```sh
python3 lead-probes/go/xml/wrapper-gates/check.py
```

The command builds the probe image, replays each lead twice per control without network access, and writes [the receipt](../../../../data/go/xml/wrapper-gates-check.json): what each package returned and which of its own coverage blocks differ between the two controls. It runs no malformed input and no fuzz campaign.
