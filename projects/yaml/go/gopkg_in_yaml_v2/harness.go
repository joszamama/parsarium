package yamlharness

import (
	"bytes"
	"encoding/json"
	"fmt"
	"strconv"

	"gopkg.in/yaml.v2"
)

// ordered receives one decoded YAML node through yaml.v2's documented
// Unmarshaler hook. A sequence decodes into []ordered (each element recurses),
// a mapping into yaml.MapSlice (yaml.v2 keeps source order and decodes nested
// mappings as MapSlice too), and anything else into interface{}.
type ordered struct{ tree any }

func (node *ordered) UnmarshalYAML(unmarshal func(any) error) error {
	var sequence []ordered
	if err := unmarshal(&sequence); err == nil && sequence != nil {
		items := make([]any, 0, len(sequence))
		for _, item := range sequence {
			items = append(items, nullable(item.tree))
		}
		node.tree = []any{"seq", items}
		return nil
	}
	var mapping yaml.MapSlice
	if err := unmarshal(&mapping); err == nil && mapping != nil {
		tree, err := typed(mapping, 0)
		node.tree = tree
		return err
	}
	var value any
	if err := unmarshal(&value); err != nil {
		return err
	}
	tree, err := typed(value, 0)
	node.tree = tree
	return err
}

// Parse decodes one local YAML document with yaml.Unmarshal and returns the
// typed tree: ["map", [[key, node]...]], ["seq", [...]], ["str", s],
// ["int", decimal], ["float", shortest decimal], ["bool", b], ["null"].
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	var root ordered
	if err := yaml.Unmarshal(data, &root); err != nil {
		return nil, err
	}
	return map[string]any{"tree": nullable(root.tree)}, nil
}

// nullable maps an untouched node to null: yaml.v2 does not call
// UnmarshalYAML for a null scalar and leaves the value at its zero state.
func nullable(tree any) any {
	if tree == nil {
		return []any{"null"}
	}
	return tree
}

func typed(value any, depth int) (any, error) {
	if depth > 64 {
		return nil, fmt.Errorf("nesting outside harness limit")
	}
	switch node := value.(type) {
	case yaml.MapSlice:
		pairs := make([]any, 0, len(node))
		for _, item := range node {
			key, ok := item.Key.(string)
			if !ok {
				return nil, fmt.Errorf("non-string mapping key")
			}
			child, err := typed(item.Value, depth+1)
			if err != nil {
				return nil, err
			}
			pairs = append(pairs, []any{key, child})
		}
		return []any{"map", pairs}, nil
	case map[any]any:
		if len(node) != 0 {
			return nil, fmt.Errorf("unordered non-empty mapping")
		}
		return []any{"map", []any{}}, nil
	case []any:
		items := make([]any, 0, len(node))
		for _, item := range node {
			child, err := typed(item, depth+1)
			if err != nil {
				return nil, err
			}
			items = append(items, child)
		}
		return []any{"seq", items}, nil
	case string:
		return []any{"str", node}, nil
	case nil:
		return []any{"null"}, nil
	case bool:
		return []any{"bool", node}, nil
	case int:
		return []any{"int", strconv.Itoa(node)}, nil
	case int64:
		return []any{"int", strconv.FormatInt(node, 10)}, nil
	case uint64:
		return []any{"int", strconv.FormatUint(node, 10)}, nil
	case float64:
		return []any{"float", strconv.FormatFloat(node, 'g', -1, 64)}, nil
	}
	return nil, fmt.Errorf("unsupported decoded value %T", value)
}

// Encode writes the result as compact JSON without HTML escaping.
func Encode(value any) string {
	var buffer bytes.Buffer
	encoder := json.NewEncoder(&buffer)
	encoder.SetEscapeHTML(false)
	if err := encoder.Encode(value); err != nil {
		panic(err)
	}
	return string(bytes.TrimRight(buffer.Bytes(), "\n"))
}
