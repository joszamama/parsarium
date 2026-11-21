package jsonharness

import (
	"fmt"
	"os"
	"reflect"
	"testing"
)

const expectedJSON = `{"arrays":3,"booleans":2,"max_depth":4,"nulls":1,"numbers":[-2.5,1,1,2,2],"objects":5,"root":"object","strings":["café \"quoted\"","go","json","parsarium","rfc8259"],"top_level_keys":["enabled","missing","name","nested","ratio","tags","version"]}`
const expectedDifferentialJSON = `{"arrays":4,"booleans":2,"max_depth":3,"nulls":1,"numbers":[0.25,1],"objects":2,"root":"array","strings":["A","two"],"top_level_items":5}`

var expectedObject = map[string]any{
	"name": "parsarium", "version": float64(1), "ratio": -2.5,
	"enabled": true, "missing": nil,
	"tags": []any{"json", "go", "rfc8259"},
	"nested": map[string]any{
		"level": float64(2),
		"items": []any{
			map[string]any{"id": float64(1), "ok": false},
			map[string]any{"id": float64(2), "text": "café \"quoted\""},
		},
		"empty": map[string]any{}, "list": []any{},
	},
}

var expectedArray = []any{
	float64(1), 0.25, "two",
	[]any{true, nil, []any{false}},
	map[string]any{"k": []any{}, "n": map[string]any{"deep": "A"}},
}

func TestControl(t *testing.T) {
	data, err := os.ReadFile("/input/control")
	if err != nil {
		t.Fatal(err)
	}
	root, err := Decode(data)
	if err != nil {
		t.Fatal(err)
	}
	// The summary is compared first so that any other valid input reports what
	// Sonic decoded; the exact tree check then still guards the control.
	got := summarize(root)
	encoded := Encode(got)
	if encoded != expectedJSON {
		t.Fatalf("control mismatch: %s", encoded)
	}
	if !reflect.DeepEqual(root, expectedObject) {
		t.Fatalf("decoded tree mismatch: %#v", root)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzJSON(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}

func TestDifferential(t *testing.T) {
	data, err := os.ReadFile("/input/differential")
	if err != nil {
		t.Fatal(err)
	}
	root, err := Decode(data)
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(root, expectedArray) {
		t.Fatalf("decoded tree mismatch: %#v", root)
	}
	got := summarize(root)
	encoded := Encode(got)
	if encoded != expectedDifferentialJSON {
		t.Fatalf("differential control mismatch: %s", encoded)
	}
}
