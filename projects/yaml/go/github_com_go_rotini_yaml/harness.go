package yamlharness

import (
	"bytes"
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/go-rotini/yaml"
)
// Parse decodes one local YAML document with yaml.UnmarshalWithOptions and
// the documented WithOrderedMap option, so every mapping arrives as a
// yaml.MapSlice in source order, and returns the typed tree:
// ["map", [[key, node]...]], ["seq", [...]], ["str", s], ["int", decimal],
// ["float", shortest decimal], ["bool", b], ["null"]. go-rotini/yaml expands
// aliases to their anchored value while decoding.

func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	var value any
	if err := yaml.UnmarshalWithOptions(data, &value, yaml.WithOrderedMap()); err != nil {
		return nil, err
	}
	tree, err := typed(value, 0)
	if err != nil {
		return nil, err
	}
	return map[string]any{"tree": tree}, nil
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
