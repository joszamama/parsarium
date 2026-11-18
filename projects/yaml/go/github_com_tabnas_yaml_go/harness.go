package yamlharness

import (
	"bytes"
	"encoding/json"
	"fmt"
	"math"
	"strconv"

	tabnas "github.com/tabnas/parser/go"
	tabnasyaml "github.com/tabnas/yaml/go"
)

// Parse parses one local YAML document with the tabnas YAML grammar plugin
// (tabnasyaml.Parse over the tabnas jsonic grammar and parser engine), which
// returns *tabnas.OrderedMap mappings (keys in source order), []any, string,
// bool, nil and float64 for every number, with aliases already copied in. It
// returns the typed tree: ["map", [[key, node]...]], ["seq", [...]],
// ["str", s], ["int", decimal], ["float", shortest decimal], ["bool", b],
// ["null"]. Because the library returns every number as float64, the harness
// types a finite integral number as int (the catalog YAML protocol rule for
// APIs without an int/float distinction); the controls contain no
// integral-valued floats.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	value, err := tabnasyaml.Parse(string(data))
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
	case *tabnas.OrderedMap:
		pairs := make([]any, 0, len(node.Keys))
		for _, key := range node.Keys {
			child, err := typed(node.Vals[key], depth+1)
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
	case float64:
		if !math.IsInf(node, 0) && !math.IsNaN(node) && node == math.Trunc(node) && math.Abs(node) < (1<<53) {
			return []any{"int", strconv.FormatInt(int64(node), 10)}, nil
		}
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
