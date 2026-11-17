# github.com/vmware/govmomi/vim25/xml — XML / Go

Pinned release: `v0.56.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, controls, and parser family](../../../../catalog/xml/go/github-com-vmware-govmomi-vim25-xml/README.md)

This is a general XML token parser from the govmomi module, not a VMware model-only decoder. Its `NewDecoder(io.Reader).Token()` implementation is a compiled fork of Go `encoding/xml` with its own `xml.go` source. The whole module archive is 12,553,438 bytes; the harness imports only `vim25/xml`.

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_vmware_govmomi_vim25_xml
python3 parsarium.py run xml go github_com_vmware_govmomi_vim25_xml controls/xml/catalog-ns.xml
python3 parsarium.py run xml go github_com_vmware_govmomi_vim25_xml controls/xml/order-default-ns.xml
python3 parsarium.py replay xml go github_com_vmware_govmomi_vim25_xml CORPUS_DIR runs/xml-govmomi-replay
python3 parsarium.py afl build xml go github_com_vmware_govmomi_vim25_xml
python3 parsarium.py afl prepare xml go github_com_vmware_govmomi_vim25_xml runs/xml-govmomi-afl
python3 projects/xml/go/github_com_vmware_govmomi_vim25_xml/verify-feedback.py
```

Replace `CORPUS_DIR` with a directory of XML files. The AFL++ command prepares a seeded run; it does not start a campaign.
