package zipharness

import (
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"testing"
)

func TestControl(t *testing.T) {
	data, err := os.ReadFile("/input/control")
	if err != nil {
		t.Fatal(err)
	}
	entries, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	got := Observed(entries)
	encoded, err := json.Marshal(got)
	if err != nil {
		t.Fatal(err)
	}
	want := Result{Name: "hello.txt", Text: "parsarium\n"}
	if !reflect.DeepEqual(got, any(want)) {
		t.Fatalf("control mismatch: %s", encoded)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzZIP(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) {
		_, _ = Parse(data)
	})
}
