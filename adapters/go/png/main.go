// Run a pinned Go PNG parser against a local, valid PNG control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"os"

	"github.com/andrianbdn/iospng"
	"github.com/anthonynsimon/bild/imgio"
	"github.com/davidbyttow/govips/v2/vips"
	"github.com/disintegration/imaging"
	pngstructure "github.com/dsoprea/go-png-image-structure/v2"
	"github.com/fogleman/gg"
	fumin "github.com/fumin/png"
	"github.com/gameparrot/fastpng"
	"github.com/gen2brain/pngn"
	goimages "github.com/go-images/png"
	"github.com/h2non/bimg"
	simplepng "github.com/knoweather/simple-png"
	scaled "github.com/m8rge/go-scaled-png"
	magical "github.com/magical/png"
	mduvall "github.com/mduvall/go-image-png/png"
	oyamo "github.com/oyamo/pngx"
	shogo "github.com/shogo82148/go-imaging/png"
	canvasimage "github.com/tdewolff/canvas/image"
	woozy "github.com/woozymasta/png"
	"gopkg.in/gographics/imagick.v3/imagick"
	tinygo "tinygo.org/x/drivers/image/png"
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
	case "github.com/disintegration/imaging":
		img, err = imaging.Open(path)
	case "github.com/fogleman/gg":
		img, err = gg.LoadPNG(path)
	case "github.com/anthonynsimon/bild/imgio":
		img, err = imgio.Open(path)
	case "github.com/gameparrot/fastpng":
		var f *os.File
		f, err = os.Open(path)
		if err == nil {
			defer f.Close()
			img, err = fastpng.Decode(f)
		}
	case "github.com/h2non/bimg":
		data, readErr := os.ReadFile(path)
		if readErr != nil {
			return nil, readErr
		}
		size, sizeErr := bimg.Size(data)
		if sizeErr != nil {
			return nil, sizeErr
		}
		return map[string]any{"width": size.Width, "height": size.Height}, nil
	case "github.com/davidbyttow/govips/v2/vips":
		if startupErr := vips.Startup(nil); startupErr != nil {
			return nil, startupErr
		}
		defer vips.Shutdown()
		ref, loadErr := vips.NewImageFromFile(path)
		if loadErr != nil {
			return nil, loadErr
		}
		defer ref.Close()
		return map[string]any{"width": ref.Width(), "height": ref.Height()}, nil
	case "gopkg.in/gographics/imagick.v3/imagick":
		data, readErr := os.ReadFile(path)
		if readErr != nil {
			return nil, readErr
		}
		imagick.Initialize()
		defer imagick.Terminate()
		wand := imagick.NewMagickWand()
		defer wand.Destroy()
		if readErr := wand.ReadImageBlob(data); readErr != nil {
			return nil, readErr
		}
		return map[string]any{"width": wand.GetImageWidth(), "height": wand.GetImageHeight()}, nil
	case "github.com/gen2brain/pngn", "github.com/go-images/png", "github.com/woozymasta/png", "github.com/m8rge/go-scaled-png", "github.com/tdewolff/canvas/image", "github.com/knoweather/simple-png", "github.com/fumin/png", "github.com/andrianbdn/iospng", "github.com/shogo82148/go-imaging/png", "github.com/magical/png", "github.com/mduvall/go-image-png/png", "github.com/oyamo/pngx", "tinygo.org/x/drivers/image/png":
		data, readErr := os.ReadFile(path)
		if readErr != nil {
			return nil, readErr
		}
		r := bytes.NewReader(data)
		switch name {
		case "github.com/gen2brain/pngn":
			img, err = pngn.Decode(r)
		case "github.com/go-images/png":
			img, err = goimages.Decode(r)
		case "github.com/shogo82148/go-imaging/png":
			img, err = shogo.Decode(r)
		case "github.com/magical/png":
			img, err = magical.Decode(r)
		case "github.com/mduvall/go-image-png/png":
			img, err = mduvall.Decode(r)
		case "github.com/oyamo/pngx":
			img, err = oyamo.Decode(r)
		case "tinygo.org/x/drivers/image/png":
			img, err = tinygo.Decode(r)
		case "github.com/woozymasta/png":
			img, err = woozy.Decode(r)
		case "github.com/m8rge/go-scaled-png":
			img, err = scaled.Decode(r, 2, 1, scaled.Box)
		case "github.com/tdewolff/canvas/image":
			var lazy *canvasimage.Image
			lazy, err = canvasimage.NewPNGImage(r)
			if err == nil {
				img, err = lazy.Image()
			}
		case "github.com/knoweather/simple-png":
			var parsed *simplepng.Png
			parsed, err = simplepng.ParsePng(r, true)
			if err == nil {
				img, err = parsed.IDATsToColor()
			}
		case "github.com/fumin/png":
			var decoder *fumin.Decoder
			decoder, err = fumin.NewDecoder(r)
			if err != nil {
				return nil, err
			}
			defer decoder.Close()
			b := decoder.Bounds()
			if b.Dx() != 2 || b.Dy() != 1 {
				return nil, fmt.Errorf("unexpected bounds: %v", b)
			}
			row, decodeErr := decoder.DecodeRow()
			if decodeErr != nil {
				return nil, decodeErr
			}
			values := make([]int, len(row))
			for i, v := range row {
				values[i] = int(v)
			}
			return map[string]any{"width": b.Dx(), "height": b.Dy(), "rgba": values}, nil
		case "github.com/andrianbdn/iospng":
			var out bytes.Buffer
			w, h, parseErr := iospng.PngRevertOptimizationWithSize(r, &out)
			if parseErr != nil {
				return nil, parseErr
			}
			return map[string]any{"width": w, "height": h, "output_bytes": out.Len()}, nil
		}
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
