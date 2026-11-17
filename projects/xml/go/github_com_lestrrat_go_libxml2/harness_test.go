package xmlharness

import (
	"os"
	"testing"
)

var controls = []struct{ file, want string }{
	{"controls/catalog-ns.xml", `{"attributes":["version=1","id=a1","{urn:parsarium:catalog}lang=es","id=b2"],"elements":["{urn:parsarium:catalog}catalog","{urn:parsarium:item}item","{urn:parsarium:item}item","{urn:parsarium:item}name","{urn:parsarium:item}note"],"max_depth":3,"namespace_declarations":2,"namespaces":["urn:parsarium:catalog","urn:parsarium:item"],"root":"{urn:parsarium:catalog}catalog","text":["Café & té","Zürich <HQ>","x < y"]}`},
	{"controls/order-default-ns.xml", `{"attributes":["n=1","{urn:parsarium:price}currency=EUR","n=2","note=say \"hi\""],"elements":["{urn:parsarium:order}order","{urn:parsarium:order}line","{urn:parsarium:order}sku","{urn:parsarium:price}amount","{urn:parsarium:order}line","plain","leaf"],"max_depth":4,"namespace_declarations":3,"namespaces":["urn:parsarium:order","urn:parsarium:price"],"root":"{urn:parsarium:order}order","text":["A-7","12.50 €"]}`},
}

func TestControls(t *testing.T) {
	for _, control := range controls {
		t.Run(control.file, func(t *testing.T) {
			input, err := os.ReadFile(control.file)
			if err != nil {
				t.Fatal(err)
			}
			got, err := Parse(input)
			if err != nil {
				t.Fatal(err)
			}
			if encoded := Encode(got); encoded != control.want {
				t.Fatalf("got %s\nwant %s", encoded, control.want)
			}
			t.Log("OBSERVED_JSON:" + Encode(got))
		})
	}
	if status := FlushNativeCoverage(); status != 0 {
		t.Fatalf("native coverage flush: %d", status)
	}
}

func FuzzXML(f *testing.F) {
	for _, control := range controls {
		input, err := os.ReadFile("/work/" + control.file)
		if err != nil {
			f.Fatal(err)
		}
		f.Add(input)
	}
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}
