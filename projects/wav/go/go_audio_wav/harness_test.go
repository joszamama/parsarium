package wavharness

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
	want := Result{SampleRate: 8000, Channels: 1, Bits: 16, Signs: []int{0, 1, -1, 0}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("control mismatch: got %+v, want %+v", got, want)
	}
	encoded, err := json.Marshal(got)
	if err != nil {
		t.Fatal(err)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzWAV(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) {
		_, _ = Parse(data)
	})
}
