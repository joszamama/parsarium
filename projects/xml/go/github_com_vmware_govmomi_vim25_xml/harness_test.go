package main

import (
	"fmt"
	"os"
	"testing"
)

const expectedJSON = `{"attributes":["version=1","id=a1","{urn:parsarium:catalog}lang=es","id=b2"],"elements":["{urn:parsarium:catalog}catalog","{urn:parsarium:item}item","{urn:parsarium:item}item","{urn:parsarium:item}name","{urn:parsarium:item}note"],"max_depth":3,"namespace_declarations":2,"namespaces":["urn:parsarium:catalog","urn:parsarium:item"],"root":"{urn:parsarium:catalog}catalog","text":["Café & té","Zürich <HQ>","x < y"]}`

func TestControl(t *testing.T) {
	data, err := os.ReadFile("/input/control")
	if err != nil {
		t.Fatal(err)
	}
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	encoded := Encode(got)
	if encoded != expectedJSON {
		t.Fatalf("control mismatch: %s", encoded)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzParser(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}

func TestDifferential(t *testing.T) {
	data, err := os.ReadFile("/input/differential")
	if err != nil {
		t.Fatal(err)
	}
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	encoded := Encode(got)
	const expected = `{"attributes":["n=1","{urn:parsarium:price}currency=EUR","n=2","note=say \"hi\""],"elements":["{urn:parsarium:order}order","{urn:parsarium:order}line","{urn:parsarium:order}sku","{urn:parsarium:price}amount","{urn:parsarium:order}line","plain","leaf"],"max_depth":4,"namespace_declarations":3,"namespaces":["urn:parsarium:order","urn:parsarium:price"],"root":"{urn:parsarium:order}order","text":["A-7","12.50 €"]}`
	if encoded != expected {
		t.Fatalf("differential mismatch: %s", encoded)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}
