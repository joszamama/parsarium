// Run one pinned Go HTTP/1.1 message parser against a local wire control.
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"github.com/evanphx/wildcat"

	"github.com/lesismal/nbio/nbhttp"
)

type byteReader struct {
	data   []byte
	offset int
}

type capturedHTTP struct {
	nbhttp.Processor
	method, target, proto string
	complete              bool
}

func (c *capturedHTTP) OnMethod(_ *nbhttp.Parser, method string)     { c.method = method }
func (c *capturedHTTP) OnURL(_ *nbhttp.Parser, target string) error  { c.target = target; return nil }
func (c *capturedHTTP) OnProto(_ *nbhttp.Parser, proto string) error { c.proto = proto; return nil }
func (c *capturedHTTP) OnComplete(_ *nbhttp.Parser)                  { c.complete = true }

func (r *byteReader) Peek(n int) ([]byte, error) {
	if n < 0 || r.offset+n > len(r.data) {
		return nil, io.EOF
	}
	return r.data[r.offset : r.offset+n], nil
}
func (r *byteReader) Skip(n int) error {
	if n < 0 || r.offset+n > len(r.data) {
		return io.EOF
	}
	r.offset += n
	return nil
}
func (r *byteReader) Release() error { return nil }
func (r *byteReader) Len() int       { return len(r.data) - r.offset }
func (r *byteReader) ReadByte() (byte, error) {
	b, err := r.Peek(1)
	if err != nil {
		return 0, err
	}
	r.offset++
	return b[0], nil
}
func (r *byteReader) ReadBinary(n int) ([]byte, error) {
	b, err := r.Peek(n)
	if err != nil {
		return nil, err
	}
	r.offset += n
	return append([]byte(nil), b...), nil
}

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	switch name {

	case "github.com/evanphx/wildcat":
		parser := wildcat.NewHTTPParser()
		if _, err := parser.Parse(data); err != nil {
			return nil, err
		}
		return map[string]any{"method": string(parser.Method), "target": string(parser.Path), "proto": string(parser.Version), "host": string(parser.Host())}, nil

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
