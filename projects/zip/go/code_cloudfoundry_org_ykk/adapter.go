// Run one pinned third-party Go ZIP reader against the supplied local archive.
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"

	ykk "code.cloudfoundry.org/ykk"
)

type output struct {
	Name string `json:"name"`
	Text string `json:"text"`
}

func readOne(count int, name string, open func() (io.ReadCloser, error)) {
	if count != 1 {
		panic(fmt.Errorf("expected one entry, got %d", count))
	}
	input, err := open()
	if err != nil {
		panic(err)
	}
	data, err := io.ReadAll(input)
	input.Close()
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(output{Name: name, Text: string(data)}); err != nil {
		panic(err)
	}
}

func readExtracted(extract func(string) error) {
	dir, err := os.MkdirTemp("", "parsarium-zip-")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(dir)
	if err := extract(dir); err != nil {
		panic(err)
	}
	entries, err := os.ReadDir(dir)
	if err != nil {
		panic(err)
	}
	if len(entries) != 1 || entries[0].IsDir() {
		panic(fmt.Errorf("expected one extracted file, got %d entries", len(entries)))
	}
	data, err := os.ReadFile(filepath.Join(dir, entries[0].Name()))
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(output{Name: entries[0].Name(), Text: string(data)}); err != nil {
		panic(err)
	}
}

func readFileSystem(fsys fs.FS) {
	entries, err := fs.ReadDir(fsys, ".")
	if err != nil {
		panic(err)
	}
	if len(entries) != 1 || entries[0].IsDir() {
		panic(fmt.Errorf("expected one ZIP entry, got %d", len(entries)))
	}
	data, err := fs.ReadFile(fsys, entries[0].Name())
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(output{Name: entries[0].Name(), Text: string(data)}); err != nil {
		panic(err)
	}
}

func openInput(path string) *os.File {
	f, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	return f
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	name, path := os.Args[1], os.Args[2]
	switch name {

	case "code.cloudfoundry.org/ykk":
		f := openInput(path)
		defer f.Close()
		stat, err := f.Stat()
		if err != nil {
			panic(err)
		}
		r, err := ykk.NewReader(f, stat.Size())
		if err != nil {
			panic(err)
		}
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)

	default:
		panic(fmt.Errorf("unsupported package: %s", name))
	}
}
