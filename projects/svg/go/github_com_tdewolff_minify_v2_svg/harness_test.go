package main

import (
    "encoding/json"
    "fmt"
    "os"
    "path/filepath"
    "reflect"
    "testing"
)

const parserName = "github.com/tdewolff/minify/v2/svg"
const expectedJSON = "{\"minified\":\"<svg xmlns=\\\"http://www.w3.org/2000/svg\\\" width=\\\"2\\\" height=\\\"1\\\" viewBox=\\\"0 0 2 1\\\"><rect x=\\\"0\\\" y=\\\"0\\\" width=\\\"1\\\" height=\\\"1\\\" fill=\\\"red\\\"/><rect x=\\\"1\\\" y=\\\"0\\\" width=\\\"1\\\" height=\\\"1\\\" fill=\\\"#0f0\\\"/></svg>\"}"

func parseControl(source string) (map[string]any, error) { data, err := os.ReadFile(source); if err != nil { return nil, err }; return run(parserName, data) }

func TestControl(t *testing.T) {
    got, err := parseControl("/input/control")
    if err != nil { t.Fatal(err) }
    encoded, err := json.Marshal(got)
    if err != nil { t.Fatal(err) }
    var observed, expected any
    if err := json.Unmarshal(encoded, &observed); err != nil { t.Fatal(err) }
    if err := json.Unmarshal([]byte(expectedJSON), &expected); err != nil { t.Fatal(err) }
    if !reflect.DeepEqual(observed, expected) { t.Fatalf("control mismatch: %s", encoded) }
    fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzParser(f *testing.F) {
    f.Fuzz(func(t *testing.T, data []byte) {
        if len(data) == 0 || len(data) > (1 << 20) { return }
        directory := t.TempDir()
        source := filepath.Join(directory, "input.svg")
        if err := os.WriteFile(source, data, 0600); err != nil { t.Fatal(err) }
        _, _ = parseControl(source)
    })
}
