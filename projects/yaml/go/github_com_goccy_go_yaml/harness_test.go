package yamlharness

import (
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"testing"
)

const expectedJSON = `{"tree":["map",[["kind",["str","catalog"]],["version",["int","2"]],["ratio",["float","0.25"]],["offset",["int","-17"]],["enabled",["bool",true]],["retired",["bool",false]],["missing",["null"]],["title",["str","Café \"quoted\"\tend"]],["single",["str","it's here"]],["tags",["seq",[["str","alpha"],["str","beta"],["str","gamma delta"]]]],["point",["map",[["lat",["int","1"]],["lon",["float","-2.5"]]]]],["items",["seq",[["map",[["id",["int","7"]],["name",["str","first item"]],["note",["str","line one\nline two\n"]]]],["map",[["id",["int","8"]],["name",["str","Zürich"]],["note",["str","folded text\n"]]]]]]],["defaults",["map",[["retries",["int","3"]],["label",["str","base"]]]]],["service",["map",[["settings",["map",[["retries",["int","3"]],["label",["str","base"]]]]],["label",["str","edge"]]]]]]]}`
const expectedDifferentialJSON = `{"tree":["seq",[["map",[["order",["str","A-7"]],["lines",["seq",[["map",[["sku",["str","Xé-1"]],["qty",["int","2"]],["price",["float","12.5"]]]],["map",[["sku",["str","B '2'"]],["qty",["int","1"]],["price",["float","0.75"]]]]]]],["flags",["seq",[]]],["meta",["map",[]]]]],["map",[["city",["str","Berlin"]],["zip",["str","10115"]]]],["map",[["city",["str","Berlin"]],["zip",["str","10115"]]]],["seq",[["int","1"],["seq",[["int","2"],["int","3"]]],["map",[["k",["str","v"]]]]]],["str","plain multi word"],["str","line\nbreak"],["str","kept\n  indented"],["null"],["bool",false]]]}`

func check(t *testing.T, path, expected string) string {
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	encoded := Encode(got)
	var observed, want any
	if err := json.Unmarshal([]byte(encoded), &observed); err != nil {
		t.Fatal(err)
	}
	if err := json.Unmarshal([]byte(expected), &want); err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(observed, want) {
		t.Fatalf("typed tree mismatch for %s: %s", path, encoded)
	}
	return encoded
}

func TestControl(t *testing.T) {
	fmt.Printf("OBSERVED_JSON:%s\n", check(t, "/input/control", expectedJSON))
}

func TestDifferential(t *testing.T) {
	check(t, "/input/differential", expectedDifferentialJSON)
}

func FuzzYAML(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}
