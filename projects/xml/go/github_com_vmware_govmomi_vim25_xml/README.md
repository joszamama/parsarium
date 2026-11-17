# github.com/vmware/govmomi/vim25/xml — XML / Go

Pinned release: `v0.56.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-vmware-govmomi-vim25-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_vmware_govmomi_vim25_xml
python3 parsarium.py run xml go github_com_vmware_govmomi_vim25_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_vmware_govmomi_vim25_xml CORPUS_DIR runs/xml-github_com_vmware_govmomi_vim25_xml-replay
python3 parsarium.py afl build xml go github_com_vmware_govmomi_vim25_xml
python3 parsarium.py afl prepare xml go github_com_vmware_govmomi_vim25_xml runs/xml-github_com_vmware_govmomi_vim25_xml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
