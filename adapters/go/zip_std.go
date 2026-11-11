// Verify Go's documented archive/zip.OpenReader on the shared valid ZIP control.
package main

import (
	"archive/zip"
	"encoding/json"
	"fmt"
	"io"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run adapters/go/zip_std.go CONTROL_PATH")
	}
	r, err := zip.OpenReader(os.Args[1])
	if err != nil {
		panic(err)
	}
	defer r.Close()
	if len(r.File) != 1 {
		panic(fmt.Errorf("expected one entry, got %d", len(r.File)))
	}
	f := r.File[0]
	input, err := f.Open()
	if err != nil {
		panic(err)
	}
	contents, err := io.ReadAll(input)
	input.Close()
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(map[string]any{"name": f.Name, "text": string(contents)}); err != nil {
		panic(err)
	}
}
