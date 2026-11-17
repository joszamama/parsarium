package tomlharness

import (
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/BurntSushi/toml"
)

// Parse decodes one TOML document with toml.Decode into map[string]any and
// rebuilds the toml-test-like typed tree from the decoded Go values.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	var document map[string]any
	if _, err := toml.Decode(string(data), &document); err != nil {
		return nil, err
	}
	tree, err := typed(document)
	if err != nil {
		return nil, err
	}
	return tree.(map[string]any), nil
}

func scalar(kind, value string) map[string]any {
	return map[string]any{"type": kind, "value": value}
}

func typed(value any) (any, error) {
	switch node := value.(type) {
	case map[string]any:
		table := make(map[string]any, len(node))
		for key, child := range node {
			converted, err := typed(child)
			if err != nil {
				return nil, err
			}
			table[key] = converted
		}
		return table, nil
	case []map[string]any:
		array := make([]any, len(node))
		for index, child := range node {
			converted, err := typed(child)
			if err != nil {
				return nil, err
			}
			array[index] = converted
		}
		return array, nil
	case []any:
		array := make([]any, len(node))
		for index, child := range node {
			converted, err := typed(child)
			if err != nil {
				return nil, err
			}
			array[index] = converted
		}
		return array, nil
	case string:
		return scalar("string", node), nil
	case int64:
		return scalar("integer", strconv.FormatInt(node, 10)), nil
	case float64:
		return scalar("float", formatFloat(node)), nil
	case bool:
		return scalar("bool", strconv.FormatBool(node)), nil
	case time.Time:
		// BurntSushi/toml returns local values in fixed zones named
		// datetime-local, date-local and time-local (internal/tz.go); its own
		// toml-test tagger (internal/tag/add.go) tells them apart the same way.
		switch node.Location().String() {
		case "datetime-local":
			return scalar("datetime-local", node.Format("2006-01-02T15:04:05.999999999")), nil
		case "date-local":
			return scalar("date-local", node.Format("2006-01-02")), nil
		case "time-local":
			return scalar("time-local", node.Format("15:04:05.999999999")), nil
		}
		return scalar("datetime", node.UTC().Format("2006-01-02T15:04:05.999999999Z")), nil
	}
	return nil, fmt.Errorf("unsupported decoded value %T", value)
}

func formatFloat(value float64) string {
	if math.IsInf(value, 0) || math.IsNaN(value) {
		return strconv.FormatFloat(value, 'g', -1, 64)
	}
	text := strconv.FormatFloat(value, 'f', -1, 64)
	if !strings.Contains(text, ".") {
		text += ".0"
	}
	return text
}

// Encode writes the typed tree as sorted-key JSON without calling a JSON library.
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
	case []any:
		parts := make([]string, len(node))
		for index, item := range node {
			parts[index] = Encode(item)
		}
		return "[" + strings.Join(parts, ",") + "]"
	case string:
		return quote(node)
	}
	panic(fmt.Sprintf("unsupported tree value %T", value))
}

func quote(text string) string {
	var builder strings.Builder
	builder.WriteByte('"')
	for _, character := range text {
		switch character {
		case '"', '\\':
			builder.WriteByte('\\')
			builder.WriteRune(character)
		case '\n':
			builder.WriteString(`\n`)
		case '\t':
			builder.WriteString(`\t`)
		case '\r':
			builder.WriteString(`\r`)
		case '\b':
			builder.WriteString(`\b`)
		case '\f':
			builder.WriteString(`\f`)
		default:
			if character < 0x20 {
				fmt.Fprintf(&builder, "\\u%04x", character)
			} else {
				builder.WriteRune(character)
			}
		}
	}
	builder.WriteByte('"')
	return builder.String()
}
