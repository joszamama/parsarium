package xmlharness

import (
	"bytes"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/beego/x2j"
)

// Parse summarizes the maps produced by x2j's documented local APIs. The
// []byte and string paths (Unmarshal into a map, ByteDocToMap, DocToMap)
// first delete whitespace before every '<' in the raw document and must agree
// with each other. ToMap(io.Reader) skips that rewrite, so it is summarized
// separately.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	unmarshaled := map[string]any{}
	if err := x2j.Unmarshal(data, &unmarshaled); err != nil {
		return nil, err
	}
	fromBytes, err := x2j.ByteDocToMap(data)
	if err != nil {
		return nil, err
	}
	fromString, err := x2j.DocToMap(string(data))
	if err != nil {
		return nil, err
	}
	fromReader, err := x2j.ToMap(bytes.NewReader(data))
	if err != nil {
		return nil, err
	}
	byteResult, err := summarize(unmarshaled)
	if err != nil {
		return nil, err
	}
	for _, other := range []map[string]any{fromBytes, fromString} {
		result, err := summarize(other)
		if err != nil {
			return nil, err
		}
		if Encode(result) != Encode(byteResult) {
			return nil, fmt.Errorf("Unmarshal, ByteDocToMap and DocToMap maps differ")
		}
	}
	readerResult, err := summarize(fromReader)
	if err != nil {
		return nil, err
	}
	return map[string]any{"bytes": byteResult, "reader": readerResult}, nil
}

// summary flattens x2j's map convention: "-name" keys are attributes,
// "#text" is character data beside attributes or children, any other key is
// a child element, and a repeated key (element or "#text") becomes a
// []interface{} value.
type summary struct {
	rootName   string
	elements   []string
	attributes []string
	text       []string
	empty      []string
	lists      []string
	maxDepth   int
}

func summarize(m map[string]any) (map[string]any, error) {
	if len(m) != 1 {
		return nil, fmt.Errorf("map has %d root keys", len(m))
	}
	s := &summary{}
	for name, value := range m {
		s.rootName = name
		s.element(name, value, 1)
	}
	return s.result(), nil
}

func (s *summary) element(path string, value any, depth int) {
	switch node := value.(type) {
	case []any:
		s.lists = append(s.lists, path+"="+strconv.Itoa(len(node)))
		for index, item := range node {
			s.single(path+"["+strconv.Itoa(index)+"]", item, depth)
		}
	default:
		s.single(path, node, depth)
	}
}

func (s *summary) single(path string, value any, depth int) {
	s.elements = append(s.elements, path)
	s.maxDepth = max(s.maxDepth, depth)
	switch node := value.(type) {
	case map[string]any:
		for key, child := range node {
			switch {
			case key == "#text":
				s.textValue(path+"/#text", child)
			case strings.HasPrefix(key, "-"):
				s.attributes = append(s.attributes, path+"/"+key+"="+scalar(child))
			default:
				s.element(path+"/"+key, child, depth+1)
			}
		}
	case string:
		if node == "" {
			s.empty = append(s.empty, path)
		} else {
			s.text = append(s.text, path+"="+node)
		}
	default:
		s.text = append(s.text, path+"="+scalar(node))
	}
}

func (s *summary) textValue(path string, value any) {
	runs, ok := value.([]any)
	if !ok {
		s.text = append(s.text, path+"="+scalar(value))
		return
	}
	s.lists = append(s.lists, path+"="+strconv.Itoa(len(runs)))
	for index, run := range runs {
		s.text = append(s.text, path+"["+strconv.Itoa(index)+"]="+scalar(run))
	}
}

func scalar(value any) string {
	if text, ok := value.(string); ok {
		return text
	}
	return fmt.Sprintf("%T:%v", value, value)
}

func (s *summary) result() map[string]any {
	for _, list := range [][]string{s.elements, s.attributes, s.text, s.empty, s.lists} {
		sort.Strings(list)
	}
	return map[string]any{
		"attributes":     append([]string{}, s.attributes...),
		"elements":       append([]string{}, s.elements...),
		"empty_elements": append([]string{}, s.empty...),
		"lists":          append([]string{}, s.lists...),
		"max_depth":      s.maxDepth,
		"root":           s.rootName,
		"text":           append([]string{}, s.text...),
	}
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
