package pnmharness

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
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	want := Result{Width: 2, Height: 1, RGB0: []int{255, 0, 0}, RGB1: []int{0, 255, 0}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("control mismatch: got %+v, want %+v", got, want)
	}
	encoded, err := json.Marshal(got)
	if err != nil {
		t.Fatal(err)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzPNM(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) {
		_, _ = Parse(data)
	})
}
