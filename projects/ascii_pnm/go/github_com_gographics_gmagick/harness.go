// Package gmagickpnm decodes one local ASCII PNM byte slice through the
// pinned gmagick GraphicsMagick binding (MagickWand.ReadImageBlob).
package gmagickpnm

import (
	"encoding/json"
	"sync"

	"github.com/gographics/gmagick"
)

type Summary struct {
	Width  uint   `json:"width"`
	Height uint   `json:"height"`
	Format string `json:"format"`
	Colors uint   `json:"colors"`
}

var initialize sync.Once

func Parse(data []byte) (Summary, error) {
	initialize.Do(gmagick.Initialize)
	wand := gmagick.NewMagickWand()
	defer wand.Destroy()
	if err := wand.ReadImageBlob(data); err != nil {
		return Summary{}, err
	}
	return Summary{Width: wand.GetImageWidth(), Height: wand.GetImageHeight(),
		Format: wand.GetImageFormat(), Colors: wand.GetImageColors()}, nil
}

func Encode(summary Summary) string {
	encoded, err := json.Marshal(summary)
	if err != nil {
		panic(err)
	}
	return string(encoded)
}
