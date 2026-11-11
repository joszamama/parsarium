// Run one pinned third-party Go ZIP reader against the supplied local archive.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"

	ykk "code.cloudfoundry.org/ykk"
	starry "github.com/STARRY-S/zip"
	alex "github.com/alexmullins/zip"
	andrew "github.com/andrewarchi/archive"
	unpack "github.com/c4milo/unpackit"
	extract "github.com/codeclysm/extract/v4"
	zipexe "github.com/daaku/go.zipexe"
	evil "github.com/evilsocket/islazy/zip"
	unarr "github.com/gen2brain/go-unarr"
	gitarchives "github.com/git-pkgs/archives"
	safe "github.com/google/safearchive/zip"
	hillu "github.com/hillu/go-archive-zip-crypto"
	klaus "github.com/klauspost/compress/zip"
	streamzip "github.com/krolaw/zipstream"
	archives "github.com/mholt/archives"
	nmiyake "github.com/nmiyake/archiver"
	archivefile "github.com/pierrre/archivefile/zip"
	sagan "github.com/sagan/zip"
	lazy "github.com/sourcegraph/lazyzip"
	caezip "github.com/unknwon/cae/zip"
	unxed "github.com/unxed/zip"
	xy "github.com/xyproto/unzip"
	yeka "github.com/yeka/zip"
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
	case "github.com/klauspost/compress/zip":
		r, err := klaus.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/yeka/zip":
		r, err := yeka.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/alexmullins/zip":
		r, err := alex.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/STARRY-S/zip":
		r, err := starry.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/unxed/zip":
		r, err := unxed.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/sagan/zip":
		r, err := sagan.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/google/safearchive/zip":
		r, err := safe.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/hillu/go-archive-zip-crypto":
		r, err := hillu.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
	case "github.com/sourcegraph/lazyzip":
		r, err := lazy.OpenReader(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		f, err := r.Next()
		if err != nil {
			panic(err)
		}
		_, nextErr := r.Next()
		if nextErr != io.EOF {
			panic(fmt.Errorf("expected exactly one entry: %v", nextErr))
		}
		readOne(1, f.Name, f.Open)
	case "github.com/evilsocket/islazy/zip":
		readExtracted(func(dir string) error { _, err := evil.Unzip(path, dir); return err })
	case "github.com/xyproto/unzip":
		readExtracted(func(dir string) error { return xy.Extract(path, dir) })
	case "github.com/krolaw/zipstream":
		f := openInput(path)
		defer f.Close()
		r := streamzip.NewReader(f)
		header, err := r.Next()
		if err != nil {
			panic(err)
		}
		data, err := io.ReadAll(r)
		if err != nil {
			panic(err)
		}
		if _, err = r.Next(); err != io.EOF {
			panic(fmt.Errorf("expected one entry: %v", err))
		}
		if err := json.NewEncoder(os.Stdout).Encode(output{Name: header.Name, Text: string(data)}); err != nil {
			panic(err)
		}
	case "github.com/pierrre/archivefile/zip":
		readExtracted(func(dir string) error { return archivefile.UnarchiveFile(path, dir, nil) })
	case "github.com/unknwon/cae/zip":
		readExtracted(func(dir string) error { return caezip.ExtractTo(path, dir) })
	case "github.com/nmiyake/archiver":
		readExtracted(func(dir string) error { return nmiyake.Unzip(path, dir) })
	case "github.com/codeclysm/extract/v4":
		readExtracted(func(dir string) error {
			f := openInput(path)
			defer f.Close()
			return extract.Zip(context.Background(), f, dir, nil)
		})
	case "github.com/git-pkgs/archives":
		f := openInput(path)
		defer f.Close()
		r, err := gitarchives.Open(path, f)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		entries, err := r.List()
		if err != nil {
			panic(err)
		}
		if len(entries) != 1 {
			panic(fmt.Errorf("expected one entry, got %d", len(entries)))
		}
		readOne(1, entries[0].Name, func() (io.ReadCloser, error) { return r.Extract(entries[0].Path) })
	case "github.com/mholt/archives":
		f, err := archives.FileSystem(context.Background(), path, nil)
		if err != nil {
			panic(err)
		}
		readFileSystem(f)
	case "github.com/andrewarchi/archive":
		r, filename, err := andrew.OpenSingleFileZip(path)
		if err != nil {
			panic(err)
		}
		readOne(1, filename, func() (io.ReadCloser, error) { return r, nil })
	case "github.com/c4milo/unpackit":
		readExtracted(func(dir string) error { f := openInput(path); defer f.Close(); return unpack.Unzip(f, dir) })
	case "github.com/daaku/go.zipexe":
		closer, r, err := zipexe.OpenCloser(path)
		if err != nil {
			panic(err)
		}
		defer closer.Close()
		readOne(len(r.File), r.File[0].Name, r.File[0].Open)
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
	case "github.com/gen2brain/go-unarr":
		r, err := unarr.NewArchive(path)
		if err != nil {
			panic(err)
		}
		defer r.Close()
		entries, err := r.List()
		if err != nil {
			panic(err)
		}
		if len(entries) != 1 {
			panic(fmt.Errorf("expected one entry, got %d", len(entries)))
		}
		if err := r.EntryFor(entries[0]); err != nil {
			panic(err)
		}
		data, err := r.ReadAll()
		if err != nil {
			panic(err)
		}
		if err := json.NewEncoder(os.Stdout).Encode(output{Name: entries[0], Text: string(data)}); err != nil {
			panic(err)
		}
	default:
		panic(fmt.Errorf("unsupported package: %s", name))
	}
}
