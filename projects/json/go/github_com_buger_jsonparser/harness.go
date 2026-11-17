package jsonharness

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/buger/jsonparser"
)

// Parse walks the JSON structure using jsonparser's local byte APIs.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	raw, kind, _, err := jsonparser.Get(data)
	if err != nil {
		return nil, err
	}
	value, err := materialize(raw, kind)
	if err != nil {
		return nil, err
	}
	return summarize(value), nil
}

func materialize(raw []byte, kind jsonparser.ValueType) (any, error) {
	switch kind {
	case jsonparser.Object:
		object := make(map[string]any)
		err := jsonparser.ObjectEach(raw, func(key, value []byte, childKind jsonparser.ValueType, _ int) error {
			child, err := materialize(value, childKind)
			if err == nil { object[string(key)] = child }
			return err
		})
		return object, err
	case jsonparser.Array:
		array := make([]any, 0)
		_, err := jsonparser.ArrayEachErr(raw, func(value []byte, childKind jsonparser.ValueType, _ int, callbackErr error) error {
			if callbackErr != nil { return callbackErr }
			child, err := materialize(value, childKind)
			if err == nil { array = append(array, child) }
			return err
		})
		return array, err
	case jsonparser.String:
		return jsonparser.ParseString(raw)
	case jsonparser.Number:
		return jsonparser.ParseFloat(raw)
	case jsonparser.Boolean:
		return jsonparser.ParseBoolean(raw)
	case jsonparser.Null:
		return nil, nil
	default:
		return nil, fmt.Errorf("unrecognized JSON value type %v", kind)
	}
}

func summarize(root any) map[string]any {
	result := map[string]any{"objects": 0, "arrays": 0, "booleans": 0, "nulls": 0}
	strs := []string{}
	numbers := []float64{}
	depth := 0
	var walk func(any, int)
	walk = func(value any, level int) {
		switch node := value.(type) {
		case map[string]any:
			result["objects"] = result["objects"].(int) + 1
			depth = max(depth, level+1)
			for _, child := range node {
				walk(child, level+1)
			}
		case []any:
			result["arrays"] = result["arrays"].(int) + 1
			depth = max(depth, level+1)
			for _, child := range node {
				walk(child, level+1)
			}
		case string:
			strs = append(strs, node)
		case float64:
			numbers = append(numbers, node)
		case bool:
			result["booleans"] = result["booleans"].(int) + 1
		case nil:
			result["nulls"] = result["nulls"].(int) + 1
		}
	}
	walk(root, 0)
	sort.Strings(strs)
	sort.Float64s(numbers)
	result["strings"] = strs
	result["numbers"] = numbers
	result["max_depth"] = depth
	switch node := root.(type) {
	case map[string]any:
		keys := make([]string, 0, len(node))
		for key := range node {
			keys = append(keys, key)
		}
		sort.Strings(keys)
		result["root"] = "object"
		result["top_level_keys"] = keys
	case []any:
		result["root"] = "array"
		result["top_level_items"] = len(node)
	default:
		result["root"] = "scalar"
	}
	return result
}

// Encode writes the summary as canonical JSON without calling a JSON library.
func Encode(value any) string {
	switch node := value.(type) {
	case map[string]any:
		keys := make([]string, 0, len(node))
		for key := range node {
			keys = append(keys, key)
		}
		sort.Strings(keys)
		parts := make([]string, len(keys))
		for index, key := range keys {
			parts[index] = quote(key) + ":" + Encode(node[key])
		}
		return "{" + strings.Join(parts, ",") + "}"
	case []string:
		parts := make([]string, len(node))
		for index, item := range node {
			parts[index] = quote(item)
		}
		return "[" + strings.Join(parts, ",") + "]"
	case []float64:
		parts := make([]string, len(node))
		for index, item := range node {
			parts[index] = strconv.FormatFloat(item, 'g', -1, 64)
		}
		return "[" + strings.Join(parts, ",") + "]"
	case int:
		return strconv.Itoa(node)
	case string:
		return quote(node)
	}
	panic(fmt.Sprintf("unsupported summary value %T", value))
}

func quote(text string) string {
	var builder strings.Builder
	builder.WriteByte('"')
	for _, character := range text {
		switch {
		case character == '"' || character == '\\':
			builder.WriteByte('\\')
			builder.WriteRune(character)
		case character < 0x20:
			fmt.Fprintf(&builder, "\\u%04x", character)
		default:
			builder.WriteRune(character)
		}
	}
	builder.WriteByte('"')
	return builder.String()
}
