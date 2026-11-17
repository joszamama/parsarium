package probe

// Valid-control probes for Go XML leads that wrap encoding/xml or lex XML
// themselves. Each test parses PARSARIUM_CASE through the package's documented
// local API and prints what the package returned; check.py runs every test
// once per control with -coverpkg set to that package only.

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"testing"

	sdom "github.com/VictorLowther/simplexml/dom"
	xj "github.com/basgys/goxml2json"
	quickxml "github.com/dgrr/quickxml"
	x2m "github.com/sbabiv/xml2map"
	xmldom "github.com/subchen/go-xmldom"
)

func input(t *testing.T) []byte {
	data, err := os.ReadFile(os.Getenv("PARSARIUM_CASE"))
	if err != nil {
		t.Fatal(err)
	}
	return data
}

func emit(t *testing.T, value any) {
	encoded, err := json.Marshal(value)
	if err != nil {
		t.Fatal(err)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

// goxml2json: decode only (NewDecoder.Decode), the XML-parsing half of Convert.
func TestGoxml2jsonDecode(t *testing.T) {
	root := &xj.Node{}
	if err := xj.NewDecoder(bytes.NewReader(input(t))).Decode(root); err != nil {
		t.Fatal(err)
	}
	var walk func(label string, node *xj.Node) any
	walk = func(label string, node *xj.Node) any {
		children := map[string]any{}
		for name, list := range node.Children {
			items := []any{}
			for _, child := range list {
				items = append(items, walk(name, child))
			}
			children[name] = items
		}
		return map[string]any{"data": node.Data, "children": children}
	}
	emit(t, walk("", root))
}

// goxml2json: the documented Convert(io.Reader) API (decode plus JSON encode).
func TestGoxml2jsonConvert(t *testing.T) {
	out, err := xj.Convert(bytes.NewReader(input(t)))
	if err != nil {
		t.Fatal(err)
	}
	var decoded any
	if err := json.Unmarshal(out.Bytes(), &decoded); err != nil {
		t.Fatal(err)
	}
	emit(t, decoded)
}

func TestSimplexmlDom(t *testing.T) {
	doc, err := sdom.Parse(bytes.NewReader(input(t)))
	if err != nil {
		t.Fatal(err)
	}
	var walk func(element *sdom.Element) any
	walk = func(element *sdom.Element) any {
		children := []any{}
		for _, child := range element.Children() {
			children = append(children, walk(child))
		}
		attributes := []string{}
		for _, attribute := range element.Attributes {
			attributes = append(attributes, "{"+attribute.Name.Space+"}"+attribute.Name.Local+"="+attribute.Value)
		}
		return map[string]any{"name": "{" + element.Name.Space + "}" + element.Name.Local,
			"attributes": attributes, "content": string(element.Content), "children": children}
	}
	emit(t, walk(doc.Root()))
}

func TestGoXmldom(t *testing.T) {
	doc, err := xmldom.Parse(bytes.NewReader(input(t)))
	if err != nil {
		t.Fatal(err)
	}
	var walk func(node *xmldom.Node) any
	walk = func(node *xmldom.Node) any {
		children := []any{}
		for _, child := range node.Children {
			children = append(children, walk(child))
		}
		attributes := []string{}
		for _, attribute := range node.Attributes {
			attributes = append(attributes, attribute.Name+"="+attribute.Value)
		}
		return map[string]any{"name": node.Name, "attributes": attributes, "text": node.Text, "children": children}
	}
	emit(t, walk(doc.Root))
}

func TestXml2map(t *testing.T) {
	m, err := x2m.NewDecoder(bytes.NewReader(input(t))).Decode()
	if err != nil {
		t.Fatal(err)
	}
	emit(t, m)
}

func TestQuickxml(t *testing.T) {
	reader := quickxml.NewReader(bytes.NewReader(input(t)))
	events := []string{}
	for reader.Next() {
		switch element := reader.Element().(type) {
		case *quickxml.StartElement:
			attributes := ""
			element.Attrs().Range(func(kv *quickxml.KV) {
				attributes += " " + kv.Key() + "=" + kv.Value()
			})
			events = append(events, "start "+element.Name()+attributes)
		case *quickxml.EndElement:
			events = append(events, "end "+element.Name())
		case *quickxml.TextElement:
			events = append(events, "text "+element.String())
		}
	}
	emit(t, events)
}
