package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

const parserName = "github.com/faiface/beep/mp3"
const expectedJSON = "{\"sample_rate\":44100,\"length_samples\":12672,\"streamed_samples\":12672,\"samples_sha256\":\"99899cf5f832a09cd132845fb0e2a388e1f56d13388e769d2b6ffd6cee5091f5\"}"

const differentialJSON = "{\"sample_rate\":22050,\"length_samples\":6912,\"streamed_samples\":6912,\"samples_sha256\":\"ff01cf7013876ecde516b170e1c6769e49e1850d6b1226ba0f94d28184c55041\"}"

func TestControl(t *testing.T) {
	checkControl(t, "/input/control", expectedJSON)
}

// TestDifferentialControl checks the second valid control, an MPEG-2 joint
// stereo stream; it runs only when selected explicitly.
func TestDifferentialControl(t *testing.T) {
	checkControl(t, "/input/differential", differentialJSON)
}

func checkControl(t *testing.T, path, expectedJSON string) {
	got, err := run(parserName, path)
	if err != nil {
		t.Fatal(err)
	}
	encoded, err := json.Marshal(got)
	if err != nil {
		t.Fatal(err)
	}
	var observed, expected any
	if err := json.Unmarshal(encoded, &observed); err != nil {
		t.Fatal(err)
	}
	if err := json.Unmarshal([]byte(expectedJSON), &expected); err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(observed, expected) {
		t.Fatalf("control mismatch: %s", encoded)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzParser(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 || len(data) > (1<<20) {
			return
		}
		directory := t.TempDir()
		source := filepath.Join(directory, "input.mp3")
		if err := os.WriteFile(source, data, 0600); err != nil {
			t.Fatal(err)
		}
		_, _ = run(parserName, source)
	})
}
