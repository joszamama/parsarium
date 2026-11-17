# YAML controls

Hand-written YAML 1.2 documents, one per file. Every plain scalar types the same
under YAML 1.1 resolvers and the YAML 1.2 core schema; see the
[cell protocol](../../catalog/yaml/PROTOCOL.md) for the restriction.

| Control | Bytes | SHA-256 | Use |
| --- | ---: | --- | --- |
| `catalog.yaml` | 483 | `b574210db4f284734fe62b59833b24f53c99e6b5948d9d5e379f1c1439ac8d5d` | Primary control, block-mapping root |
| `order.yaml` | 345 | `a7d81a704bf582a1f54b1bcb4dfe1c68a62718e5cfc3196ccd406e4ec36bc935` | AFL++ differential control, block-sequence root |

`python3 controls/yaml/check_controls.py --require-psych` checks the hashes, the
scalar restriction and the hand-written typed trees, and cross-checks the trees
with Ruby Psych (libyaml family). Its `EXPECTED` trees are the oracle every
harness compares against.
