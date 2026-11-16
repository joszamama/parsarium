// Run a pinned Go PNG parser against a local, valid PNG control.
package main

import (
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"os"

	pngstructure "github.com/dsoprea/go-png-image-structure/v2"
)

func pixels(img image.Image) map[string]any {
	b := img.Bounds()
	values := make([]int, 0, b.Dx()*b.Dy()*4)
	for y := b.Min.Y; y < b.Max.Y; y++ {
		for x := b.Min.X; x < b.Max.X; x++ {
			c := color.NRGBAModel.Convert(img.At(x, y)).(color.NRGBA)
			values = append(values, int(c.R), int(c.G), int(c.B), int(c.A))
		}
	}
	return map[string]any{"width": b.Dx(), "height": b.Dy(), "rgba": values}
}

func run(name, path string) (map[string]any, error) {
	var img image.Image
	var err error
	switch name {

	case "github.com/dsoprea/go-png-image-structure/v2":
		parser := pngstructure.NewPngMediaParser()
		var context interface{}
		context, err = parser.ParseFile(path)
		if err != nil {
			return nil, err
		}
		chunks, ok := context.(*pngstructure.ChunkSlice)
		if !ok {
			return nil, fmt.Errorf("unexpected PNG context %T", context)
		}
		types := make([]string, 0)
		var width, height uint32
		for _, chunk := range chunks.Chunks() {
			if !chunk.CheckCrc32() {
				return nil, fmt.Errorf("invalid CRC in %s", chunk.Type)
			}
			types = append(types, chunk.Type)
			if chunk.Type == "IHDR" {
				decoded, decodeErr := pngstructure.NewChunkDecoder().Decode(chunk)
				if decodeErr != nil {
					return nil, decodeErr
				}
				header, ok := decoded.(*pngstructure.ChunkIHDR)
				if !ok {
					return nil, fmt.Errorf("unexpected IHDR %T", decoded)
				}
				width, height = header.Width, header.Height
			}
		}
		return map[string]any{"width": width, "height": height, "chunks": types}, nil
	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
	if err != nil {
		return nil, err
	}
	return pixels(img), nil
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
