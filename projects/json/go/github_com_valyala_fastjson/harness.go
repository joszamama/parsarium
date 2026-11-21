package jsonharness

import (
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"

	"github.com/valyala/fastjson"
)

// Parse walks a complete JSON document through fastjson's local byte API.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	var parser fastjson.Parser
	root, err := parser.ParseBytes(data)
	if err != nil {
		return nil, err
	}
	value, err := materialize(root)
	if err != nil {
		return nil, err
	}
	return summarize(value), nil
}

func materialize(value *fastjson.Value) (any, error) {
	switch value.Type() {
	case fastjson.TypeObject:
		objectValue, err := value.Object()
		if err != nil { return nil, err }
		object := make(map[string]any)
		var visitErr error
		objectValue.Visit(func(key []byte, childValue *fastjson.Value) {
			if visitErr != nil { return }
			child, err := materialize(childValue)
			if err != nil { visitErr = err; return }
			object[string(key)] = child
		})
		return object, visitErr
	case fastjson.TypeArray:
		arrayValue, err := value.Array()
		if err != nil { return nil, err }
		array := make([]any, 0)
		for _, childValue := range arrayValue {
			child, err := materialize(childValue)
			if err != nil { return nil, err }
			array = append(array, child)
		}
		return array, nil
	case fastjson.TypeString:
		decoded, err := value.StringBytes()
		return string(decoded), err
	case fastjson.TypeNumber:
		return value.Float64()
	case fastjson.TypeTrue:
		return true, nil
	case fastjson.TypeFalse:
		return false, nil
	case fastjson.TypeNull:
		return nil, nil
	default:
		return nil, fmt.Errorf("unrecognized JSON value type %v", value.Type())
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
			parts[index] = formatNumber(item)
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

// formatNumber writes a float64 as a JSON number. An out-of-range exponent the
// parser turned into an infinity is written as Infinity/-Infinity (NaN as NaN),
// tokens the observer's JSON reader accepts, instead of Go's "+Inf".
func formatNumber(value float64) string {
	switch {
	case math.IsNaN(value):
		return "NaN"
	case math.IsInf(value, 1):
		return "Infinity"
	case math.IsInf(value, -1):
		return "-Infinity"
	}
	return strconv.FormatFloat(value, 'g', -1, 64)
}
