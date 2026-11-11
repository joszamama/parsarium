// Run one pinned Go PDF reader against the valid, one-page local control.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os"

	leijacob "gitee.com/leijacob/pdf"
	ajroetker "github.com/ajroetker/pdf"
	asposepdf "github.com/aspose-pdf-foss/aspose-pdf-foss-for-go"
	benoit "github.com/benoitkugler/pdf/reader"
	casibase "github.com/casibase/pdf"
	dcu "github.com/dcu/pdf"
	digitorus "github.com/digitorus/pdf"
	dslipak "github.com/dslipak/pdf"
	fitz "github.com/gen2brain/go-fitz"
	giraffes "github.com/giraffesyo/pdf"
	pdfextract "github.com/go-pdfkit/extract"
	pdfkit "github.com/go-pdfkit/reader"
	ledongthuc "github.com/ledongthuc/pdf"
	oneplus "github.com/oneplus1000/pdf"
	"github.com/pdfcpu/pdfcpu/pkg/api"
	"github.com/phpdave11/gofpdi"
	registrobr "github.com/registrobr/pdf"
	unicore "github.com/unidoc/unidoc/pdf/core"
	rsc "rsc.io/pdf"
	seehuhn "seehuhn.de/go/pdf"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	pageCount := 0
	var err error
	switch name {
	case "github.com/ledongthuc/pdf":
		var doc *ledongthuc.Reader
		doc, err = ledongthuc.NewReader(r, int64(len(data)))
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "rsc.io/pdf":
		var doc *rsc.Reader
		doc, err = rsc.NewReader(r, int64(len(data)))
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "github.com/digitorus/pdf":
		var doc *digitorus.Reader
		doc, err = digitorus.NewReader(r, int64(len(data)))
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "github.com/dslipak/pdf":
		var doc *dslipak.Reader
		doc, err = dslipak.NewReader(r, int64(len(data)))
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "github.com/go-pdfkit/reader":
		var doc *pdfkit.Document
		doc, err = pdfkit.Open(data)
		if err == nil {
			pageCount = doc.PageCount()
		}
	case "github.com/pdfcpu/pdfcpu/pkg/api":
		pageCount, err = api.PageCount(context.Background(), r, nil)
	case "github.com/phpdave11/gofpdi":
		var stream io.ReadSeeker = r
		imp := gofpdi.NewImporter()
		imp.SetSourceStream(&stream)
		pageCount = imp.GetNumPages()
	case "github.com/giraffesyo/pdf":
		var doc *giraffes.Document
		doc, err = giraffes.Extract(context.Background(), r, int64(len(data)))
		if err == nil {
			pageCount = doc.PageCount
		}
	case "github.com/benoitkugler/pdf/reader":
		doc, _, parseErr := benoit.ParsePDFReader(r, benoit.Options{})
		err = parseErr
		if err == nil {
			pageCount = doc.Catalog.Pages.Count()
		}
	case "github.com/gen2brain/go-fitz":
		doc, openErr := fitz.NewFromMemory(data)
		err = openErr
		if err == nil {
			defer doc.Close()
			pageCount = doc.NumPage()
		}
	case "github.com/aspose-pdf-foss/aspose-pdf-foss-for-go":
		doc, openErr := asposepdf.OpenStream(r)
		err = openErr
		if err == nil {
			pageCount = doc.PageCount()
		}
	case "github.com/go-pdfkit/extract":
		doc, openErr := pdfkit.Open(data)
		err = openErr
		if err == nil {
			value, textErr := pdfextract.Text(doc, 1)
			if textErr != nil {
				return nil, textErr
			}
			return map[string]any{"text": value}, nil
		}
	case "github.com/unidoc/unidoc/pdf/core":
		parser, parseErr := unicore.NewParser(r)
		err = parseErr
		if err == nil {
			return map[string]any{"objects": len(parser.GetObjectNums())}, nil
		}
	case "seehuhn.de/go/pdf":
		doc, openErr := seehuhn.NewReader(r, int64(len(data)), nil)
		err = openErr
		if err == nil {
			defer doc.Close()
			return map[string]any{"version": doc.GetMeta().Version.String()}, nil
		}
	case "github.com/casibase/pdf":
		doc, openErr := casibase.NewReader(r, int64(len(data)))
		err = openErr
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "github.com/dcu/pdf":
		doc, openErr := dcu.NewReader(r, int64(len(data)))
		err = openErr
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "github.com/ajroetker/pdf":
		doc, openErr := ajroetker.NewReader(r, int64(len(data)))
		err = openErr
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "github.com/oneplus1000/pdf":
		doc, openErr := oneplus.NewReader(r, int64(len(data)))
		err = openErr
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "gitee.com/leijacob/pdf":
		doc, openErr := leijacob.NewReader(r, int64(len(data)))
		err = openErr
		if err == nil {
			pageCount = doc.NumPage()
		}
	case "github.com/registrobr/pdf":
		doc, openErr := registrobr.NewReader(r, int64(len(data)))
		err = openErr
		if err == nil {
			pageCount = doc.NumPage()
		}
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
