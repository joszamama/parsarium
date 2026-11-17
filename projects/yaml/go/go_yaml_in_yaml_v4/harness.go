package yamlharness

import (
	"bytes"
	"encoding/json"
	"fmt"
	"strconv"

	"go.yaml.in/yaml/v4"
)

// Parse loads one local YAML document with the v4 yaml.Load API (default v4
// options) into a yaml.Node tree and returns the typed tree:
// ["map", [[key, node]...]], ["seq", [...]], ["str", s], ["int", decimal],
// ["float", shortest decimal], ["bool", b], ["null"]. Aliases are expanded to
// their anchored node.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	var document yaml.Node
	if err := yaml.Load(data, &document); err != nil {
		return nil, err
	}
	if document.Kind != yaml.DocumentNode || len(document.Content) != 1 {
		return nil, fmt.Errorf("expected one YAML document")
	}
	tree, err := typed(document.Content[0], 0)
	if err != nil {
		return nil, err
	}
	return map[string]any{"tree": tree}, nil
}

func typed(node *yaml.Node, depth int) (any, error) {
	if depth > 64 {
		return nil, fmt.Errorf("nesting outside harness limit")
	}
	switch node.Kind {
	case yaml.AliasNode:
		return typed(node.Alias, depth+1)
	case yaml.MappingNode:
		pairs := make([]any, 0, len(node.Content)/2)
		for index := 0; index+1 < len(node.Content); index += 2 {
			key := node.Content[index]
			if key.Kind != yaml.ScalarNode || key.ShortTag() != "!!str" {
				return nil, fmt.Errorf("non-string mapping key")
			}
			value, err := typed(node.Content[index+1], depth+1)
			if err != nil {
				return nil, err
			}
			pairs = append(pairs, []any{key.Value, value})
		}
		return []any{"map", pairs}, nil
	case yaml.SequenceNode:
		items := make([]any, 0, len(node.Content))
		for _, child := range node.Content {
			value, err := typed(child, depth+1)
			if err != nil {
				return nil, err
			}
			items = append(items, value)
		}
		return []any{"seq", items}, nil
	case yaml.ScalarNode:
		switch node.ShortTag() {
		case "!!str":
			return []any{"str", node.Value}, nil
		case "!!null":
			return []any{"null"}, nil
		case "!!bool":
			var value bool
			if err := node.Load(&value); err != nil {
				return nil, err
			}
			return []any{"bool", value}, nil
		case "!!int":
			var value int64
			if err := node.Load(&value); err != nil {
				return nil, err
			}
			return []any{"int", strconv.FormatInt(value, 10)}, nil
		case "!!float":
			var value float64
			if err := node.Load(&value); err != nil {
				return nil, err
			}
			return []any{"float", strconv.FormatFloat(value, 'g', -1, 64)}, nil
		}
		return nil, fmt.Errorf("unsupported scalar tag %s", node.ShortTag())
	}
	return nil, fmt.Errorf("unsupported node kind %v", node.Kind)
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
