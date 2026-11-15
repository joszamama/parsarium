package zipharness

import (
	"bytes"
	"io"

	"github.com/klauspost/compress/zip"
)

type Result struct {
	Name string `json:"name"`
	Text string `json:"text"`
}

// Parse reads a ZIP archive from supplied bytes and observes a decoded member.
func Parse(data []byte) (Result, error) {
	r, err := zip.NewReader(bytes.NewReader(data), int64(len(data)))
	if err != nil {
		return Result{}, err
	}
	if len(r.File) == 0 {
		return Result{}, nil
	}
	f := r.File[0]
	member, err := f.Open()
	if err != nil {
		return Result{}, err
	}
	defer member.Close()
	content, err := io.ReadAll(io.LimitReader(member, 1<<20))
	if err != nil {
		return Result{}, err
	}
	return Result{Name: f.Name, Text: string(content)}, nil
}
