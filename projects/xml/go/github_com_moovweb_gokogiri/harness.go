package xmlharness

import (
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	x "github.com/moovweb/gokogiri/xml"
)

type Summary struct {
	Root                  string   `json:"root"`
	Elements              []string `json:"elements"`
	Attributes            []string `json:"attributes"`
	Namespaces            []string `json:"namespaces"`
	NamespaceDeclarations int      `json:"namespace_declarations"`
	MaxDepth              int      `json:"max_depth"`
	Text                  []string `json:"text"`
}

func name(uri, local string) string {
	if uri == "" {
		return local
	}
	return "{" + uri + "}" + local
}

func visit(node x.Node, depth int, result *Summary, namespaces map[string]bool) {
	switch node.NodeType() {
	case x.XML_ELEMENT_NODE:
		label := name(node.Namespace(), node.Name())
		result.Elements = append(result.Elements, label)
		if depth == 1 {
			result.Root = label
		}
		if depth > result.MaxDepth {
			result.MaxDepth = depth
		}
		if node.Namespace() != "" {
			namespaces[node.Namespace()] = true
		}
		for _, declaration := range node.DeclaredNamespaces() {
			result.NamespaceDeclarations++
			if declaration.Uri != "" {
				namespaces[declaration.Uri] = true
			}
		}
		attributes := node.Attributes()
		keys := make([]string, 0, len(attributes))
		for key := range attributes {
			keys = append(keys, key)
		}
		sort.Strings(keys)
		for _, key := range keys {
			attribute := attributes[key]
			result.Attributes = append(result.Attributes, name(attribute.Namespace(), attribute.Name())+"="+attribute.Value())
			if attribute.Namespace() != "" {
				namespaces[attribute.Namespace()] = true
			}
		}
		for child := node.FirstChild(); child != nil; child = child.NextSibling() {
			visit(child, depth+1, result, namespaces)
		}
	case x.XML_TEXT_NODE, x.XML_CDATA_SECTION_NODE:
		if text := strings.TrimSpace(node.Content()); text != "" {
			result.Text = append(result.Text, text)
		}
	}
}

// Parse invokes gokogiri's byte parser and reports only data returned by its DOM API.
func Parse(data []byte) (Summary, error) {
	if len(data) == 0 || len(data) > 1<<20 {
		return Summary{}, fmt.Errorf("input outside 1 MiB harness limit")
	}
	document, err := x.Parse(data, x.DefaultEncodingBytes, nil, x.XML_PARSE_NONET|x.XML_PARSE_NOCDATA, nil)
	if err != nil {
		return Summary{}, err
	}
	defer document.Free()
	root := document.Root()
	if root == nil {
		return Summary{}, fmt.Errorf("no XML root")
	}
	result := Summary{Elements: []string{}, Attributes: []string{}, Namespaces: []string{}, Text: []string{}}
	namespaces := map[string]bool{}
	visit(root, 1, &result, namespaces)
	for uri := range namespaces {
		result.Namespaces = append(result.Namespaces, uri)
	}
	sort.Strings(result.Namespaces)
	return result, nil
}

func Encode(result Summary) string {
	bytes, err := json.Marshal(result)
	if err != nil {
		panic(err)
	}
	return string(bytes)
}
