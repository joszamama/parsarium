package xmlharness

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	xmlx "github.com/go-forks/go-pkg-xmlx"
)

// Parse loads local bytes through the documented Document.LoadBytes API and
// summarizes the node tree that xmlx built: element and attribute names come
// from Node.Name / Attr.Name (encoding/xml expanded names), text from
// NT_TEXT node values, and comment / processing-instruction nodes end a text run.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	doc := xmlx.New()
	if err := doc.LoadBytes(data, nil); err != nil {
		return nil, err
	}
	if doc.Root == nil {
		return nil, fmt.Errorf("document has no root node")
	}
	s := &summary{namespaces: map[string]bool{}}
	for _, child := range doc.Root.Children {
		s.walk(child, 1)
	}
	s.flush()
	return s.result()
}

type summary struct {
	elements     []string
	attributes   []string
	namespaces   map[string]bool
	declarations int
	maxDepth     int
	text         []string
	run          strings.Builder
}

func (s *summary) walk(node *xmlx.Node, depth int) {
	switch node.Type {
	case xmlx.NT_ELEMENT:
		s.flush()
		s.elements = append(s.elements, clark(node.Name.Space, node.Name.Local))
		s.maxDepth = max(s.maxDepth, depth)
		for _, attr := range node.Attributes {
			if attr.Name.Space == "xmlns" || (attr.Name.Space == "" && attr.Name.Local == "xmlns") {
				s.declarations++
				if attr.Value != "" {
					s.namespaces[attr.Value] = true
				}
				continue
			}
			s.attributes = append(s.attributes, clark(attr.Name.Space, attr.Name.Local)+"="+attr.Value)
		}
		for _, child := range node.Children {
			s.walk(child, depth+1)
		}
		s.flush()
	case xmlx.NT_TEXT:
		s.run.WriteString(node.Value)
	default:
		// NT_COMMENT, NT_PROCINST and NT_DIRECTIVE nodes end a character-data run.
		s.flush()
	}
}

func (s *summary) flush() {
	if segment := strings.TrimSpace(s.run.String()); segment != "" {
		s.text = append(s.text, segment)
	}
	s.run.Reset()
}

func (s *summary) result() (map[string]any, error) {
	if len(s.elements) == 0 {
		return nil, fmt.Errorf("document has no root element")
	}
	namespaces := make([]string, 0, len(s.namespaces))
	for uri := range s.namespaces {
		namespaces = append(namespaces, uri)
	}
	sort.Strings(namespaces)
	return map[string]any{
		"attributes":             append([]string{}, s.attributes...),
		"elements":               s.elements,
		"max_depth":              s.maxDepth,
		"namespace_declarations": s.declarations,
		"namespaces":             namespaces,
		"root":                   s.elements[0],
		"text":                   append([]string{}, s.text...),
	}, nil
}

func clark(space, local string) string {
	if space == "" {
		return local
	}
	return "{" + space + "}" + local
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
