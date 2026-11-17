package xmlharness

import (
	"fmt"
	"os"
	"testing"
)

// Raw leaf Content keeps entity and character references and CDATA markup:
// xmltree exposes no decoded character data.
const expectedJSON = `{"attribute_qnames":["version=1","id=a1","c:lang=es","id=b2"],"attributes":["version=1","id=a1","{urn:parsarium:catalog}lang=es","id=b2"],"element_qnames":["c:catalog","item","item","name","note"],"elements":["{urn:parsarium:catalog}catalog","{urn:parsarium:item}item","{urn:parsarium:item}item","{urn:parsarium:item}name","{urn:parsarium:item}note"],"leaf_content":["{urn:parsarium:item}item=Café &amp; té","{urn:parsarium:item}name=Zürich &lt;HQ&gt;","{urn:parsarium:item}note=<![CDATA[x < y]]>"],"max_depth":3,"name_namespaces":["urn:parsarium:catalog","urn:parsarium:item"],"root":"{urn:parsarium:catalog}catalog"}`

const differentialJSON = `{"attribute_qnames":["n=1","p:currency=EUR","n=2","note=say \"hi\""],"attributes":["n=1","{urn:parsarium:price}currency=EUR","n=2","note=say \"hi\""],"element_qnames":["order","line","sku","p:amount","line","plain","leaf"],"elements":["{urn:parsarium:order}order","{urn:parsarium:order}line","{urn:parsarium:order}sku","{urn:parsarium:price}amount","{urn:parsarium:order}line","plain","leaf"],"leaf_content":["{urn:parsarium:order}sku=A&#x2D;7","{urn:parsarium:price}amount=12&#46;50 &#x20AC;","leaf="],"max_depth":4,"name_namespaces":["urn:parsarium:order","urn:parsarium:price"],"root":"{urn:parsarium:order}order"}`

func check(t *testing.T, variable, fallback, expected, label string) {
	path := os.Getenv(variable)
	if path == "" {
		path = fallback
	}
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	encoded := Encode(got)
	if encoded != expected {
		t.Fatalf("%s mismatch: %s", label, encoded)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func TestControl(t *testing.T) {
	check(t, "PARSARIUM_CONTROL", "/input/control", expectedJSON, "control")
}

func TestDifferential(t *testing.T) {
	check(t, "PARSARIUM_DIFFERENTIAL", "/input/differential", differentialJSON, "differential")
}

func FuzzXML(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}
