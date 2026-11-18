// Run one pinned third-party Go ZIP reader against the supplied local archive.
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"

	alex "github.com/alexmullins/zip"
)

// entry is one archive member as the library exposed it. A directory read
// through an extracted tree or an fs.FS has a trailing slash and no text.
type entry struct {
	Name string  `json:"name"`
	Text *string `json:"text,omitempty"`
}

// emit prints the single entry of a one-entry archive as an object, and any
// other number of entries as an array of the same objects in read order.
func emit(entries []entry) {
	var value any = entries
	if len(entries) == 1 {
		value = entries[0]
	}
	if err := json.NewEncoder(os.Stdout).Encode(value); err != nil {
		panic(err)
	}
}

func fileEntry(name string, data []byte) entry {
	text := string(data)
	return entry{Name: name, Text: &text}
}

func readEach(count int, name func(int) string, open func(int) (io.ReadCloser, error)) {
	entries := []entry{}
	for index := 0; index < count; index++ {
		input, err := open(index)
		if err != nil {
			panic(err)
		}
		data, err := io.ReadAll(input)
		input.Close()
		if err != nil {
			panic(err)
		}
		entries = append(entries, fileEntry(name(index), data))
	}
	emit(entries)
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
	entries := []entry{}
	err = filepath.WalkDir(dir, func(path string, item fs.DirEntry, err error) error {
		if err != nil || path == dir {
			return err
		}
		relative, err := filepath.Rel(dir, path)
		if err != nil {
			return err
		}
		relative = filepath.ToSlash(relative)
		if item.IsDir() {
			entries = append(entries, entry{Name: relative + "/"})
			return nil
		}
		data, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		entries = append(entries, fileEntry(relative, data))
		return nil
	})
	if err != nil {
		panic(err)
	}
	emit(entries)
}

func readFileSystem(fsys fs.FS) {
	entries := []entry{}
	err := fs.WalkDir(fsys, ".", func(path string, item fs.DirEntry, err error) error {
		if err != nil || path == "." {
			return err
		}
		if item.IsDir() {
			entries = append(entries, entry{Name: path + "/"})
			return nil
		}
		data, err := fs.ReadFile(fsys, path)
		if err != nil {
			return err
		}
		entries = append(entries, fileEntry(path, data))
		return nil
	})
	if err != nil {
		panic(err)
	}
	emit(entries)
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

	case "github.com/alexmullins/zip":
		r, err := alex.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readEach(len(r.File), func(i int) string { return r.File[i].Name }, func(i int) (io.ReadCloser, error) { return r.File[i].Open() })

	default:
		panic(fmt.Errorf("unsupported package: %s", name))
	}
}
