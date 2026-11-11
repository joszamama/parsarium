// Run one pinned Go ASCII PNM decoder against a valid local P1, P2, or P3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"os"

	picset "codeberg.org/rabenauge/picsetgo/formats/netpbm"
	media "github.com/571451370/go-media/image/pnm"
	uno "github.com/UNO-SOFT/gopnm"
	gfxcodec "github.com/go-gfx/gfx/codec"
	harry "github.com/harrydb/go/img/pnm"
	hexaflex "github.com/hexaflex/pnm"
	jbuchbinder "github.com/jbuchbinder/gopnm"
	jcbritobr "github.com/jcbritobr/pnm"
	kovid "github.com/kovidgoyal/imaging/netpbm"
	ncruces "github.com/ncruces/go-pnm"
	peterh "github.com/peterh/go/img/pnm"
	shogo "github.com/shogo82148/go-imaging/pnm"
	"github.com/spakin/netpbm"
	wkqco "github.com/wkqco33/tdraw/pnm"
	"gopkg.in/gographics/imagick.v3/imagick"
)

func pixels(img image.Image) map[string]any {
	b := img.Bounds()
	a := color.NRGBAModel.Convert(img.At(b.Min.X, b.Min.Y)).(color.NRGBA)
	z := color.NRGBAModel.Convert(img.At(b.Min.X+1, b.Min.Y)).(color.NRGBA)
	return map[string]any{"width": b.Dx(), "height": b.Dy(), "rgb0": []int{int(a.R), int(a.G), int(a.B)}, "rgb1": []int{int(z.R), int(z.G), int(z.B)}}
}

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	var img image.Image
	var err error
	switch name {
	case "github.com/jbuchbinder/gopnm":
		img, err = jbuchbinder.Decode(r)
	case "github.com/spakin/netpbm":
		img, err = netpbm.Decode(r, nil)
	case "github.com/UNO-SOFT/gopnm":
		img, err = uno.Decode(r)
	case "github.com/hexaflex/pnm":
		img, err = hexaflex.Decode(r)
	case "github.com/wkqco33/tdraw/pnm":
		img, err = wkqco.Decode(r)
	case "github.com/shogo82148/go-imaging/pnm":
		img, err = shogo.Decode(r)
	case "github.com/ncruces/go-pnm":
		img, err = ncruces.Decode(r)
	case "github.com/harrydb/go/img/pnm":
		img, err = harry.Decode(r)
	case "github.com/peterh/go/img/pnm":
		img, err = peterh.Decode(r)
	case "github.com/571451370/go-media/image/pnm":
		img, err = media.Decode(r)
	case "github.com/kovidgoyal/imaging/netpbm":
		img, err = kovid.Decode(r)
	case "codeberg.org/rabenauge/picsetgo/formats/netpbm":
		img, err = picset.Decode(r)
	case "github.com/jcbritobr/pnm":
		parsed := jcbritobr.NewPPMImage(0, 0, 0, jcbritobr.PPMText)
		if err := jcbritobr.NewDecoder(r, jcbritobr.PPMText).Decode(parsed); err != nil {
			return nil, err
		}
		return map[string]any{"width": parsed.Width(), "height": parsed.Height(), "maxval": parsed.Value()}, nil
	case "github.com/go-gfx/gfx/codec":
		decoded, decodeErr := gfxcodec.Decode(data)
		if decodeErr != nil {
			return nil, decodeErr
		}
		img = decoded.ToNRGBA()
	case "gopkg.in/gographics/imagick.v3/imagick":
		imagick.Initialize()
		defer imagick.Terminate()
		wand := imagick.NewMagickWand()
		defer wand.Destroy()
		if readErr := wand.ReadImageBlob(data); readErr != nil {
			return nil, readErr
		}
		return map[string]any{"width": wand.GetImageWidth(), "height": wand.GetImageHeight()}, nil
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
