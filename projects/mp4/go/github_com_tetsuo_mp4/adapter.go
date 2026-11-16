// Run one pinned Go MP4 parser against the valid local MP4 control.
package main

import (
	"bytes"

	"encoding/json"
	"fmt"
	"io"
	"os"

	tetsuo "github.com/tetsuo/mp4"
)

type rangeReader struct{ data []byte }

func (r rangeReader) RangeRead(start, length uint64) (io.ReadCloser, error) {
	return io.NopCloser(io.NewSectionReader(bytes.NewReader(r.data), int64(start), int64(length))), nil
}

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	switch name {
	case "github.com/tetsuo/mp4":
		reader := tetsuo.NewReader(data)
		for reader.Next() {
			if reader.Type() == tetsuo.TypeFtyp {
				ftyp := tetsuo.ReadFtyp(reader.Data())
				return map[string]any{"brand": string(ftyp.MajorBrand[:])}, nil
			}
		}
		return nil, fmt.Errorf("missing ftyp")

	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	result, err := run(os.Args[1], os.Args[2])
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
