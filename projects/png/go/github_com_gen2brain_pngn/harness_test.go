package main

import (
    "encoding/json"
    "fmt"
    "os"
    "path/filepath"
    "reflect"
    "testing"
)

const parserName = "github.com/gen2brain/pngn"
const expectedJSON = "{\"height\":1,\"rgba\":[255,0,0,255,0,255,0,255],\"width\":2}"

func TestControl(t *testing.T) {
    got, err := run(parserName, "/input/control")
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
        source := filepath.Join(directory, "input.png")
        if err := os.WriteFile(source, data, 0600); err != nil { t.Fatal(err) }
        _, _ = run(parserName, source)
    })
}
