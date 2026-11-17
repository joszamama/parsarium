package sqlharness

import (
	"fmt"
	"os"
	"testing"
)

const expectedJSON = `{"statement_count":1,"statements":[{"functions":["count","sum"],"group_by":1,"joins":1,"kind":"select","literals":[["number","10"],["string","paid"]],"order_by":1,"select_items":3,"tables":["customers","orders"],"where":true}]}`
const expectedDifferentialJSON = `{"statement_count":1,"statements":[{"columns":4,"kind":"insert","literals":[["number","1"],["number","19.5"],["number","2"],["number","250"],["number","42"],["number","7"],["string","open"],["string","paid"]],"rows":2,"tables":["orders"]}]}`

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
	if status := FlushNativeCoverage(); status != 0 {
		t.Fatalf("native coverage flush: %d", status)
	}
}

func FuzzSQL(f *testing.F) {
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
	if encoded != expectedDifferentialJSON {
		t.Fatalf("differential control mismatch: %s", encoded)
	}
}
