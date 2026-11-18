package yamlharness

import (
	"bytes"
	"encoding/json"
	"fmt"
	"strconv"

	pyaml "github.com/yongjohnlee80/golib/parse/yaml"
	"github.com/yongjohnlee80/golib/yaml"
)

// Parse parses one local YAML stream with the golib parse/yaml parser
// (pyaml.Parse: event stream composed into a node tree, no tag resolution),
// requires exactly one document, and evaluates it with the same module's
// golib/yaml package under the YAML 1.2 Core schema (yaml.Evaluate with
// yaml.Core), which constructs nil, bool, int64, float64, string, []any and
// yaml.Map (mapping entries in source order). It returns the typed tree:
// ["map", [[key, node]...]], ["seq", [...]], ["str", s], ["int", decimal],
// ["float", shortest decimal], ["bool", b], ["null"]. Aliases bound by the
// parser are constructed as their anchored value by Evaluate.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	stream, err := pyaml.Parse(data)
	if err != nil {
		return nil, err
	}
	if len(stream.Docs) != 1 {
		return nil, fmt.Errorf("expected one YAML document")
	}
	value, err := yaml.Evaluate(stream.Docs[0], yaml.Core)
	if err != nil {
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
	case yaml.Map:
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
