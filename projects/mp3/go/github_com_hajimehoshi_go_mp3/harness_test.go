package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

const parserName = "github.com/hajimehoshi/go-mp3"
const expectedJSON = "{\"sample_rate\":44100,\"length_bytes\":50688,\"decoded_bytes\":50688,\"pcm_sha256\":\"18a327dc0181f97f5702af2a35900734e04a0f0bee3091e77580dfe5b8397304\"}"

const differentialJSON = "{\"sample_rate\":22050,\"length_bytes\":27648,\"decoded_bytes\":27648,\"pcm_sha256\":\"454a8580b026f4b35026042df3e21768beb3b9fc1f1f1037701902abab2ea0a9\"}"

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
