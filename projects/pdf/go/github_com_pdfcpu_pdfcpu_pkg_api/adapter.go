// Run one pinned Go PDF reader against the valid, one-page local control.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"

	"os"

	"github.com/pdfcpu/pdfcpu/pkg/api"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	pageCount := 0
	var err error
	switch name {

	case "github.com/pdfcpu/pdfcpu/pkg/api":
		pageCount, err = api.PageCount(context.Background(), r, nil)

	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
	if err != nil {
		return nil, err
	}
	return map[string]any{"pages": pageCount}, nil
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	result, err := run(os.Args[1], data)
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
