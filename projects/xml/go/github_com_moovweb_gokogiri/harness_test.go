package xmlharness

import (
	"encoding/json"
	"os"
	"reflect"
	"testing"
)

var controls = []struct{ file, want string }{
	{"controls/catalog-ns.xml", `{"root":"{urn:parsarium:catalog}catalog","elements":["{urn:parsarium:catalog}catalog","{urn:parsarium:item}item","{urn:parsarium:item}item","{urn:parsarium:item}name","{urn:parsarium:item}note"],"attributes":["version=1","id=a1","{urn:parsarium:catalog}lang=es","id=b2"],"namespaces":["urn:parsarium:catalog","urn:parsarium:item"],"namespace_declarations":2,"max_depth":3,"text":["Café & té","Zürich <HQ>","x < y"]}`},
	{"controls/order-default-ns.xml", `{"root":"{urn:parsarium:order}order","elements":["{urn:parsarium:order}order","{urn:parsarium:order}line","{urn:parsarium:order}sku","{urn:parsarium:price}amount","{urn:parsarium:order}line","plain","leaf"],"attributes":["{urn:parsarium:price}currency=EUR","n=1","n=2","note=say \"hi\""],"namespaces":["urn:parsarium:order","urn:parsarium:price"],"namespace_declarations":3,"max_depth":4,"text":["A-7","12.50 €"]}`},
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
			var want Summary
			if err := json.Unmarshal([]byte(control.want), &want); err != nil {
				t.Fatal(err)
			}
			if !reflect.DeepEqual(got, want) {
				t.Fatalf("got %s\nwant %s", Encode(got), control.want)
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
