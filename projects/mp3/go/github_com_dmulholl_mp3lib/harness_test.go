package main

import (
    "encoding/json"
    "fmt"
    "os"
    "reflect"
    "testing"
)

const expectedJSON = `{"sample_rate":44100,"channels":1,"frames":11,"frame_bytes":2298,"samples_per_frame":1152,"bitrate":64000}`

func TestControl(t *testing.T) {
    data, err := os.ReadFile("/input/control")
    if err != nil { t.Fatal(err) }
    got, err := parse(data)
    if err != nil { t.Fatal(err) }
    encoded, err := json.Marshal(got)
    if err != nil { t.Fatal(err) }
    var observed, expected any
    if err := json.Unmarshal(encoded, &observed); err != nil { t.Fatal(err) }
    if err := json.Unmarshal([]byte(expectedJSON), &expected); err != nil { t.Fatal(err) }
    if !reflect.DeepEqual(observed, expected) { t.Fatalf("control mismatch: %s", encoded) }
    fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func TestDifferentialControl(t *testing.T) {
    data, err := os.ReadFile("/input/differential")
    if err != nil { t.Fatal(err) }
    got, err := parse(data)
    if err != nil { t.Fatal(err) }
    encoded, err := json.Marshal(got)
    if err != nil { t.Fatal(err) }
    const want = `{"sample_rate":22050,"channels":2,"frames":12,"frame_bytes":1254,"samples_per_frame":576,"bitrate":32000}`
    var observed, expected any
    if err := json.Unmarshal(encoded, &observed); err != nil { t.Fatal(err) }
    if err := json.Unmarshal([]byte(want), &expected); err != nil { t.Fatal(err) }
    if !reflect.DeepEqual(observed, expected) { t.Fatalf("differential control mismatch: %s", encoded) }
    fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func FuzzParser(f *testing.F) {
    f.Fuzz(func(t *testing.T, data []byte) {
        if len(data) == 0 || len(data) > 1<<20 { return }
        _, _ = parse(data)
    })
}
