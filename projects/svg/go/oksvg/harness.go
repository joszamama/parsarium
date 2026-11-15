package svgharness

import (
    "bytes"
    "github.com/srwiley/oksvg"
)

type Result struct {
    Paths int `json:"paths"`
    Width float64 `json:"width"`
}

func Parse(data []byte) (Result, error) {
    icon, err := oksvg.ReadIconStream(bytes.NewReader(data))
    if err != nil { return Result{}, err }
    return Result{Paths: len(icon.SVGPaths), Width: icon.ViewBox.W}, nil
}
