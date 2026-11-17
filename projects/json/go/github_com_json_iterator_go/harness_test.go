package jsonharness

import (
	"fmt"
	"os"
	"testing"
)

const expectedJSON = `{"arrays":3,"booleans":2,"max_depth":4,"nulls":1,"numbers":[-2.5,1,1,2,2],"objects":5,"root":"object","strings":["café \"quoted\"","go","json","parsarium","rfc8259"],"top_level_keys":["enabled","missing","name","nested","ratio","tags","version"]}`

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

func FuzzJSON(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}
