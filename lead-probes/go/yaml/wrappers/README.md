# Go YAML lead checks — round 2

This is a reproducible **unselected lead probe**, not a Parsarium parser project. It records why the Go YAML leads below the selected paths are not counted.

- `main.go` runs one lead's documented API on one valid control: `github.com/ghodss/yaml`, `sigs.k8s.io/yaml` and `k8s.io/apimachinery/pkg/util/yaml` (JSON conversion; their typed tree keeps the key order of the JSON text they emit), `github.com/knadh/koanf/parsers/yaml` and `github.com/kylelemons/go-gypsy/yaml` (map-based results; Go map keys are reported sorted), `sigs.k8s.io/kustomize/kyaml/yaml` (`Parse`, walking the wrapped `yaml.Node`) and `cuelang.org/go/encoding/yaml` (`Extract`, walking the CUE AST).
- `check.py` compares each result with the hand-written oracle of `controls/yaml/check_controls.py`; for the two leads that match it builds the probe with `go build -cover` (main package included in `-coverpkg`) and compares the covered blocks of the lead's own packages and of `go.yaml.in/yaml/v3` between the controls, three runs each. It also downloads the fork, predecessor and rename leads and counts distinct non-test source lines shared with the selected go-yaml module.

From the repository root:

```sh
python3 lead-probes/go/yaml/wrappers/check.py
```

The command writes [the observation](../../../../data/go/yaml/lead-check.json). It uses the local Go toolchain and the pinned `go.sum`, runs only the two valid controls, and runs no malformed-input probe or fuzz campaign.
