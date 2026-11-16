// Run one pinned Go MP4 parser against the valid local MP4 control.
package main

import (
	"bytes"

	"encoding/json"
	"fmt"
	"io"
	"os"

	eyevinn "github.com/Eyevinn/mp4ff/mp4"
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
	r := bytes.NewReader(data)
	switch name {

	case "github.com/Eyevinn/mp4ff/mp4":
		file, err := eyevinn.DecodeFile(r)
		if err != nil {
			return nil, err
		}
		if file.Ftyp == nil || file.Moov == nil {
			return nil, fmt.Errorf("missing ftyp or moov")
		}
		return map[string]any{"brand": file.Ftyp.MajorBrand(), "tracks": len(file.Moov.Traks)}, nil

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
