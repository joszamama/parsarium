package xmlharness

import (
	"context"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/lestrrat-go/helium"
)

// Parse reads local bytes through helium's documented NewParser().Parse API
// with default settings and summarizes the DOM it built: element and
// attribute namespace URIs and local names, per-element namespace
// declarations (Element.Namespaces), and text / CDATA node content. Comment
// and processing-instruction nodes end a character-data run.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	doc, err := helium.NewParser().Parse(context.Background(), data)
	if err != nil {
		return nil, err
	}
	root := doc.DocumentElement()
	if root == nil {
		return nil, fmt.Errorf("document has no root element")
	}
	s := &summary{namespaces: map[string]bool{}}
	s.element(root, 1)
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

func (s *summary) element(element *helium.Element, depth int) {
	s.flush()
	s.elements = append(s.elements, clark(element.URI(), element.LocalName()))
	s.maxDepth = max(s.maxDepth, depth)
	for _, ns := range element.Namespaces() {
		s.declarations++
		if ns.URI() != "" {
			s.namespaces[ns.URI()] = true
		}
	}
	for _, attr := range element.Attributes() {
		s.attributes = append(s.attributes, clark(attr.URI(), attr.LocalName())+"="+attr.Value())
	}
	for child := element.FirstChild(); child != nil; child = child.NextSibling() {
		switch child.Type() {
		case helium.ElementNode:
			s.element(child.(*helium.Element), depth+1)
		case helium.TextNode, helium.CDATASectionNode:
			s.run.Write(child.Content())
		default:
			s.flush()
		}
	}
	s.flush()
}

func (s *summary) flush() {
	if segment := strings.TrimSpace(s.run.String()); segment != "" {
		s.text = append(s.text, segment)
	}
	s.run.Reset()
}

func (s *summary) result() (map[string]any, error) {
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
