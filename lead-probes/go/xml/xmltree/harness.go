package xmlharness

import (
	"encoding/xml"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"aqwari.net/xml/xmltree"
)

// Parse builds one tree with xmltree.Parse([]byte) and summarizes only what the
// package exposes: expanded element and attribute names from the
// encoding/xml.Decoder.Token stream it consumes, qualified names rebuilt by
// xmltree's own Scope.Prefix, and each leaf element's raw Content bytes.
// xmltree keeps no decoded character data, and it moves namespace
// declarations out of StartElement.Attr into an unexported Scope, so the
// summary reports neither decoded text nor a declaration count.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	root, err := xmltree.Parse(data)
	if err != nil {
		return nil, err
	}
	s := &summary{namespaces: map[string]bool{}}
	s.walk(root, 1)
	namespaces := make([]string, 0, len(s.namespaces))
	for uri := range s.namespaces {
		namespaces = append(namespaces, uri)
	}
	sort.Strings(namespaces)
	return map[string]any{
		"attribute_qnames": s.attributeQNames,
		"attributes":       s.attributes,
		"element_qnames":   s.elementQNames,
		"elements":         s.elements,
		"leaf_content":     s.leafContent,
		"max_depth":        s.maxDepth,
		"name_namespaces":  namespaces,
		"root":             s.elements[0],
	}, nil
}

type summary struct {
	elements        []string
	elementQNames   []string
	attributes      []string
	attributeQNames []string
	leafContent     []string
	namespaces      map[string]bool
	maxDepth        int
}

func (s *summary) walk(el *xmltree.Element, depth int) {
	s.maxDepth = max(s.maxDepth, depth)
	s.elements = append(s.elements, s.clark(el.Name))
	s.elementQNames = append(s.elementQNames, el.Prefix(el.Name))
	for _, attr := range el.StartElement.Attr {
		s.attributes = append(s.attributes, s.clark(attr.Name)+"="+attr.Value)
		s.attributeQNames = append(s.attributeQNames, el.Prefix(attr.Name)+"="+attr.Value)
	}
	if len(el.Children) == 0 {
		s.leafContent = append(s.leafContent, s.clark(el.Name)+"="+string(el.Content))
	}
	for index := range el.Children {
		s.walk(&el.Children[index], depth+1)
	}
}

func (s *summary) clark(name xml.Name) string {
	if name.Space == "" {
		return name.Local
	}
	s.namespaces[name.Space] = true
	return "{" + name.Space + "}" + name.Local
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
