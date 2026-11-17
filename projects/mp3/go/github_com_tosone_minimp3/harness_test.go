package main

import (
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"testing"
)

const primaryJSON = `{"sample_rate":44100,"channels":1,"decoded_bytes":25344,"pcm_sha256":"0641e37cb18148b29cfc23ffc8c479115a4e042a0952a91570e92888aec0a33e"}`
const variantJSON = `{"sample_rate":22050,"channels":2,"decoded_bytes":27648,"pcm_sha256":"ac01db4bb3d3c907d3b51ecaefd6497cce1a693035114377eeedef2ef5afb653"}`

func checkControl(t *testing.T, path, expectedJSON string) {
	t.Helper()
	defer func() {
		if rc := writeNativeProfile(); rc != 0 {
			t.Errorf("native profile flush failed: %d", rc)
		}
	}()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	got, err := parse(data)
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

func TestControl(t *testing.T)             { checkControl(t, "/input/control", primaryJSON) }
func TestDifferentialControl(t *testing.T) { checkControl(t, "/input/differential", variantJSON) }

func FuzzParser(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 || len(data) > 1<<20 {
			return
		}
		_, _ = parse(data)
	})
}
