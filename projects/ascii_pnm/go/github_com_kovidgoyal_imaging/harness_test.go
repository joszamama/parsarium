package main

import (
    "encoding/json"
    "fmt"
    "os"
    "path/filepath"
    "reflect"
    "testing"
)

const parserName = "github.com/kovidgoyal/imaging"
const expectedJSON = "{\"height\":1,\"rgb0\":[255,0,0],\"rgb1\":[0,255,0],\"width\":2}"

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
        source := filepath.Join(directory, "input.ppm")
        if err := os.WriteFile(source, data, 0600); err != nil { t.Fatal(err) }
        _, _ = parseControl(source)
    })
}
