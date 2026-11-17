# gokogiri XML / Go

Pinned module: `github.com/moovweb/gokogiri@v0.0.0-20180713195410-a1a828153468` (MIT). The Docker build also pins libxml2 2.15.4. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification](verification.json) · [candidate evidence](../../../../data/go/xml/gokogiri-candidate.json)

`xml.Parse([]byte, ...)` parses local XML bytes into a DOM. The adapter reports expanded element and attribute names, namespace declarations, text, and depth from DOM APIs on two valid XML controls. Gokogiri is a Go binding to the **shared native libxml2 parser family**, not an independent Go tokenizer. The source report separates 93 Go binding lines from more than 1,700 native libxml2 parser-support lines. The AFL++ image instruments native parser sources only: its parse-only probe and full DOM harness produced identical feedback maps on both controls.

The recorded pkg.go.dev metric is **108 importing packages**. It is a within-Go adoption signal, not a count of actual XML parse calls.

The 2018 module needs the pinned [compatibility patch](cgo-compat.patch) for Go 1.27 and libxml2 2.15.4. It updates a private cgo type reference, includes the C headers used by XPath, and replaces a removed libxml2 debug helper with equivalent child counting.

From the repository root:

```sh
python3 parsarium.py build xml go github_com_moovweb_gokogiri
python3 parsarium.py run xml go github_com_moovweb_gokogiri controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml go github_com_moovweb_gokogiri
python3 parsarium.py afl prepare xml go github_com_moovweb_gokogiri runs/gokogiri-xml-afl
```

The AFL++ prepare command records a launch plan and seeds; it does not start a campaign. The controls validate UTF-8 XML without DOCTYPE only.
