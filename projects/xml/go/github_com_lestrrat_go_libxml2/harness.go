package xmlharness

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/lestrrat-go/libxml2"
	"github.com/lestrrat-go/libxml2/clib"
	"github.com/lestrrat-go/libxml2/parser"
	"github.com/lestrrat-go/libxml2/types"
)

// ParseDocument runs the documented libxml2.Parse([]byte, ...parser.Option)
// entry point (xmlCtxtReadMemory through cgo) with network access forbidden.
func ParseDocument(data []byte) (types.Document, error) {
	if len(data) == 0 || len(data) > 1<<20 {
		return nil, fmt.Errorf("input outside 1 MiB harness limit")
	}
	return libxml2.Parse(data, parser.XMLParseNoNet)
}

// Parse reports only data returned by the package's types.Document / types.Element
// DOM API: NamespaceURI/LocalName, GetNamespaces (the element's own xmlns
// declarations), Attributes in document order, and text / CDATA node values.
// Comment and processing-instruction nodes end a character-data run.
func Parse(data []byte) (map[string]any, error) {
	document, err := ParseDocument(data)
	if err != nil {
		return nil, err
	}
	defer document.Free()
	root, err := document.DocumentElement()
	if err != nil {
		return nil, err
	}
	s := &summary{namespaces: map[string]bool{}}
	if err := s.visit(root, 1); err != nil {
		return nil, err
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

func (s *summary) visit(node types.Node, depth int) error {
	switch node.NodeType() {
	case clib.ElementNode:
		element, ok := node.(types.Element)
		if !ok {
			return fmt.Errorf("element node without Element API")
		}
		s.flush()
		s.elements = append(s.elements, clark(element.NamespaceURI(), element.LocalName()))
		s.maxDepth = max(s.maxDepth, depth)
		declarations, err := element.GetNamespaces()
		if err != nil {
			return err
		}
		for _, declaration := range declarations {
			s.declarations++
			if declaration.URI() != "" {
				s.namespaces[declaration.URI()] = true
			}
			declaration.Free()
		}
		attributes, err := element.Attributes()
		if err != nil {
			return err
		}
		for _, attribute := range attributes {
			// dom.Attribute exposes the XMLNode name methods beyond the types.Attribute interface.
			named, ok := attribute.(interface {
				LocalName() string
				NamespaceURI() string
			})
			if !ok {
				return fmt.Errorf("attribute node without name API")
			}
			s.attributes = append(s.attributes, clark(named.NamespaceURI(), named.LocalName())+"="+attribute.Value())
		}
		if node.HasChildNodes() {
			child, err := node.FirstChild()
			for err == nil && child != nil {
				if err := s.visit(child, depth+1); err != nil {
					return err
				}
				child, err = child.NextSibling()
			}
			if err != nil {
				return err
			}
		}
		s.flush()
	case clib.TextNode, clib.CDataSectionNode:
		s.run.WriteString(node.NodeValue())
	default:
		s.flush()
	}
	return nil
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
