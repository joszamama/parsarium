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

// Parse reads a ZIP archive from supplied bytes and returns every member in
// archive order.
func Parse(data []byte) ([]Result, error) {
	r, err := zip.NewReader(bytes.NewReader(data), int64(len(data)))
	if err != nil {
		return nil, err
	}
	entries := []Result{}
	for _, f := range r.File {
		member, err := f.Open()
		if err != nil {
			return nil, err
		}
		content, err := io.ReadAll(member)
		member.Close()
		if err != nil {
			return nil, err
		}
		entries = append(entries, Result{Name: f.Name, Text: string(content)})
	}
	return entries, nil
}

// Observed is the single entry of a one-entry archive as an object, and any
// other number of entries as an array of the same objects in archive order.
func Observed(entries []Result) any {
	if len(entries) == 1 {
		return entries[0]
	}
	return entries
}
