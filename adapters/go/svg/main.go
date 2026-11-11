// Run a pinned Go SVG parser against the valid local two-rectangle control.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"image"
	"os"
	"strings"

	"cogentcore.org/core/math32"
	cogent "cogentcore.org/core/svg"
	"github.com/JoshVarga/svgparser"
	nimble "github.com/NimbleMarkets/oksvg"
	benoit "github.com/benoitkugler/oksvg/svgicon"
	webrender "github.com/benoitkugler/webrender/svg"
	"github.com/boxesandglue/svgreader"
	excitoon "github.com/excitoon/coolsvg-go"
	fyne "github.com/fyne-io/oksvg"
	gen2brain "github.com/gen2brain/svg"
	ggsvg "github.com/go-gfx/gfx/svg"
	guiok "github.com/golang-gui/oksvg"
	ironsvg "github.com/ironpark/ggfx/svg"
	lafriks "github.com/lafriks/go-svg"
	pgavlin "github.com/pgavlin/svg2"
	rustyoz "github.com/rustyoz/svg"
	sfomuseum "github.com/sfomuseum/go-svg"
	shibukawa "github.com/shibukawa/bdf/image/svg"
	"github.com/srwiley/oksvg"
	"github.com/tdewolff/minify/v2"
	minsvg "github.com/tdewolff/minify/v2/svg"
	"github.com/vibrantgio/svg/parser"
	goki "goki.dev/svg"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	switch name {
	case "github.com/srwiley/oksvg":
		icon, err := oksvg.ReadIconStream(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.ViewBox.W, "paths": len(icon.SVGPaths)}, nil
	case "github.com/JoshVarga/svgparser":
		root, err := svgparser.Parse(r, true)
		if err != nil {
			return nil, err
		}
		return map[string]any{"root": root.Name, "rects": len(root.FindAll("rect"))}, nil
	case "github.com/boxesandglue/svgreader":
		doc, err := svgreader.Parse(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"elements": len(doc.Elements)}, nil
	case "github.com/lafriks/go-svg":
		icon, err := lafriks.Parse(r, lafriks.IgnoreErrorMode)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.Width, "paths": len(icon.SvgPaths)}, nil
	case "github.com/gen2brain/svg":
		config, err := gen2brain.DecodeConfig(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": config.Width, "height": config.Height}, nil
	case "github.com/benoitkugler/webrender/svg":
		doc, err := webrender.Parse(r, "", nil, nil)
		if err != nil {
			return nil, err
		}
		w, h := doc.DisplayedSize()
		return map[string]any{"width": w.V, "height": h.V}, nil
	case "github.com/benoitkugler/oksvg/svgicon":
		icon, err := benoit.ReadIconStream(r, benoit.IgnoreErrorMode)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.Width, "paths": len(icon.SVGPaths)}, nil
	case "github.com/go-gfx/gfx/svg":
		result, err := ggsvg.Rasterize(string(data), ggsvg.Options{Scale: 1})
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": result.Image.W, "height": result.Image.H}, nil
	case "github.com/vibrantgio/svg/parser":
		p := parser.NewParser(parser.IgnoreErrorMode)
		_, err := p.ParseStream(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": p.Width, "paths": len(p.Paths)}, nil
	case "github.com/excitoon/coolsvg-go":
		icon, err := excitoon.ReadIconStream(r)
		if err != nil {
			return nil, err
		}
		img := image.NewRGBA(image.Rect(0, 0, 2, 1))
		if err := icon.Render(img); err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.ViewBox.W, "red": img.RGBAAt(0, 0).R, "green": img.RGBAAt(1, 0).G}, nil
	case "github.com/shibukawa/bdf/image/svg":
		doc, err := shibukawa.Parse(data, nil)
		if err != nil {
			return nil, err
		}
		return map[string]any{"root": doc.Root.Name, "elements": len(doc.Root.Children)}, nil
	case "github.com/ironpark/ggfx/svg":
		doc, err := ironsvg.Parse(r)
		if err != nil {
			return nil, err
		}
		_, _, w, h := doc.ViewBox()
		return map[string]any{"width": w, "height": h}, nil
	case "github.com/pgavlin/svg2":
		config, err := pgavlin.DecodeConfig(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": config.Width, "height": config.Height}, nil
	case "github.com/rustyoz/svg":
		doc, err := rustyoz.ParseSvgFromReader(r, "control", 1)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": doc.Width, "height": doc.Height}, nil
	case "github.com/sfomuseum/go-svg":
		img, err := sfomuseum.Rasterize(context.Background(), r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": img.Bounds().Dx(), "height": img.Bounds().Dy()}, nil
	case "github.com/NimbleMarkets/oksvg":
		icon, err := nimble.ReadIconStream(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.ViewBox.W, "paths": len(icon.SVGPaths)}, nil
	case "github.com/golang-gui/oksvg":
		icon, err := guiok.ReadIconStream(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.ViewBox.W, "paths": len(icon.SVGPaths)}, nil
	case "github.com/fyne-io/oksvg":
		icon, err := fyne.ReadIconStream(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.ViewBox.W, "paths": len(icon.SVGPaths)}, nil
	case "goki.dev/svg":
		doc := goki.NewSVG(2, 1)
		if err := doc.ReadXML(r); err != nil {
			return nil, err
		}
		return map[string]any{"width": doc.Root.ViewBox.Size.X, "height": doc.Root.ViewBox.Size.Y, "elements": doc.Root.NumChildren()}, nil
	case "github.com/tdewolff/minify/v2/svg":
		var output bytes.Buffer
		if err := minsvg.Minify(minify.New(), &output, r, nil); err != nil {
			return nil, err
		}
		return map[string]any{"minified": output.String()}, nil
	case "cogentcore.org/core/svg":
		doc := cogent.NewSVG(math32.Vector2{X: 2, Y: 1})
		err := doc.ReadXML(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": doc.Root.ViewBox.Size.X, "height": doc.Root.ViewBox.Size.Y, "elements": doc.Root.NumChildren()}, nil
	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	if !strings.HasSuffix(os.Args[2], ".svg") {
		panic("expected SVG control path")
	}
	result, err := run(os.Args[1], data)
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
