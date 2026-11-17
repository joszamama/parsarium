package xmlharness

import (
	"bytes"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/clbanning/mxj"
)

// Parse summarizes the map produced by both documented local APIs:
// NewMapXml([]byte) and NewMapXmlReader(io.Reader). The two maps must agree.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	fromBytes, err := mxj.NewMapXml(data)
	if err != nil {
		return nil, err
	}
	fromReader, err := mxj.NewMapXmlReader(bytes.NewReader(data))
	if err != nil {
		return nil, err
	}
	s := &summary{}
	if err := s.root(fromBytes); err != nil {
		return nil, err
	}
	other := &summary{}
	if err := other.root(fromReader); err != nil {
		return nil, err
	}
	result := s.result()
	if Encode(result) != Encode(other.result()) {
		return nil, fmt.Errorf("NewMapXml and NewMapXmlReader maps differ")
	}
	return result, nil
}

// summary flattens mxj's map convention: "-name" keys are attributes,
// "#text" is character data beside attributes or children, any other key is
// a child element, and a repeated child name becomes a []interface{} value.
type summary struct {
	rootName   string
	elements   []string
	attributes []string
	text       []string
	empty      []string
	lists      []string
	maxDepth   int
}

func (s *summary) root(m mxj.Map) error {
	if len(m) != 1 {
		return fmt.Errorf("map has %d root keys", len(m))
	}
	for name, value := range m {
		s.rootName = name
		s.element(name, value, 1)
	}
	return nil
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
				s.text = append(s.text, path+"/#text="+scalar(child))
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
