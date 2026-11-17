# Python × XML: pilot ranking

Two third-party paths are control-verified, alongside one separately recorded standard API. Seven of nine targeted documentation leads remain unverified. The ten-path ceiling is not a quota; this is not an exhaustive most-used ranking.

The within-cell adoption signal is [PyPI Stats](https://pypistats.org/api/) `last_month` downloads excluding known mirrors, observed 2026-11-17. It is a package-level proxy, including transitive and non-XML use. Only verified third-party paths appear below.

| Rank among verified | Package | Release | Last-month downloads | Parsed scope | Family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [lxml](https://pypi.org/project/lxml/6.1.3/) | 6.1.3 | 437,507,754 | XML 1.0 UTF-8 namespace-aware tree | lxml.etree over libxml2 2.15.4 |
| 2 | [xmltodict](https://pypi.org/project/xmltodict/) | 1.0.4 | 113,615,896 | XML hierarchy, namespace, attributes, decoded text | xmltodict over CPython Expat |

The verified `xml.etree.ElementTree` standard API is [listed separately](standard.json). lxml and xmltodict use different underlying XML parser engines.

lxml's source coverage includes libxml2 `parser.c` lines 8700–8720. Its AFL++ feedback bridge excludes that line range because an address-sensitive attribute lookup varied across identical valid replays; the five-repeat control check was stable after that exclusion.
