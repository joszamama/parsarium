# github.com/vmware/govmomi/vim25/xml — XML / Go

**Pilot / incomplete format cell.** This path is verified on two valid controls; the format-wide search remains bounded and incomplete.

- **Pinned release:** `v0.56.2`
- **License:** Apache-2.0 and BSD-3-Clause (forked Go tokenizer source)
- **Parser family:** separately compiled govmomi fork of Go `encoding/xml`
- **Local input API:** `xml.NewDecoder(io.Reader).Token()` from `github.com/vmware/govmomi/vim25/xml`
- **API reference:** [Go Packages](https://pkg.go.dev/github.com/vmware/govmomi/vim25/xml@v0.56.2#NewDecoder)
- **Valid controls:** [catalog with namespaces](../../../../controls/xml/catalog-ns.xml) and [order with default namespace](../../../../controls/xml/order-default-ns.xml)
- **Evidence:** [parser record](../../../../data/go/xml/parsers.json), [control result](../../../../data/go/xml/verification.json), [AFL++ feedback](../../../../fuzzing/afl-native/xml/go/github_com_vmware_govmomi_vim25_xml/differential.json)

The observed results include expanded element and attribute names, namespace declarations, ordered elements and attributes, decoded text and CDATA, and maximum depth. The catalog control covers 290 lines in the forked `xml.go`. Repeated AFL++ traces are identical for each valid control and differ by 30 source blocks and 30 tuples on the order control; every differing block belongs to forked `xml.go`.

The saved pkg.go.dev snapshot reports 163 importing packages for `vim25/xml`. The source lock pins the 12,553,438-byte whole govmomi module archive; this metric does not measure XML-specific call frequency.

## Run

```sh
python3 parsarium.py build xml go github_com_vmware_govmomi_vim25_xml
python3 parsarium.py run xml go github_com_vmware_govmomi_vim25_xml controls/xml/catalog-ns.xml
python3 parsarium.py run xml go github_com_vmware_govmomi_vim25_xml controls/xml/order-default-ns.xml
```
