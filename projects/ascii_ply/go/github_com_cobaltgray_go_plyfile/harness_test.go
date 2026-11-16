package main

import (
    "encoding/json"
    "fmt"
    "io"
    "os"
    "path/filepath"
    "reflect"
    "testing"
)

const parserName = "github.com/cobaltgray/go-plyfile"
const expectedJSON = "{\"vertices\":3,\"last\":{\"X\":0,\"Y\":1,\"Z\":0}}"

func parseControl(source string) (map[string]any, error) {
    reader, writer, err := os.Pipe()
    if err != nil { return nil, err }
    originalStdout, originalArgs := os.Stdout, os.Args
    os.Stdout, os.Args = writer, []string{"parser", parserName, source}
    defer func() { os.Stdout, os.Args = originalStdout, originalArgs; reader.Close(); writer.Close() }()
    main()
    writer.Close()
    data, err := io.ReadAll(reader)
    if err != nil { return nil, err }
    var output map[string]any
    err = json.Unmarshal(data, &output)
    return output, err
}

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
        source := filepath.Join(directory, "input.ply")
        if err := os.WriteFile(source, data, 0600); err != nil { t.Fatal(err) }
        _, _ = parseControl(source)
    })
}
