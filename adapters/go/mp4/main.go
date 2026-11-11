// Run one pinned Go MP4 parser against the valid local MP4 control.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os"

	eyevinn "github.com/Eyevinn/mp4ff/mp4"
	mstoykov "github.com/MStoykov/mp4"
	"github.com/Sorrow446/go-mp4tag"
	abema "github.com/abema/go-mp4"
	alfg "github.com/alfg/mp4"
	deepch "github.com/deepch/vdk/format/mp4"
	"github.com/dhowden/tag"
	edgeware "github.com/edgeware/mp4ff/mp4"
	eluv "github.com/eluv-io/mp4ff/mp4"
	frolovo "github.com/frolovo22/tag"
	"github.com/gcottom/mp4meta"
	guregu "github.com/guregu/tag"
	jfbus "github.com/jfbus/mp4"
	montybay "github.com/montybay/mp4ff/mp4"
	joy4 "github.com/nareix/joy4/format/mp4"
	ntklink "github.com/ntklink/gomediautils/go-mp4"
	rcarmo "github.com/rcarmo/go-264/audio/mp4"
	tetsuo "github.com/tetsuo/mp4"
	gomedia "github.com/yapingcat/gomedia/go-mp4"
	"go4.org/media/heif/bmff"
)

type rangeReader struct{ data []byte }

func (r rangeReader) RangeRead(start, length uint64) (io.ReadCloser, error) {
	return io.NopCloser(io.NewSectionReader(bytes.NewReader(r.data), int64(start), int64(length))), nil
}

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {
	case "github.com/tetsuo/mp4":
		reader := tetsuo.NewReader(data)
		for reader.Next() {
			if reader.Type() == tetsuo.TypeFtyp {
				ftyp := tetsuo.ReadFtyp(reader.Data())
				return map[string]any{"brand": string(ftyp.MajorBrand[:])}, nil
			}
		}
		return nil, fmt.Errorf("missing ftyp")
	case "github.com/ntklink/gomediautils/go-mp4":
		tracks, err := ntklink.CreateMp4Demuxer(r).ReadHead()
		if err != nil { return nil, err }
		return map[string]any{"tracks": len(tracks)}, nil
	case "github.com/Sorrow446/go-mp4tag":
		file, err := mp4tag.Open(path)
		if err != nil { return nil, err }
		defer file.Close()
		tags, err := file.Read()
		if err != nil { return nil, err }
		return map[string]any{"title": tags.Title}, nil
	case "github.com/gcottom/mp4meta":
		tags, err := mp4meta.ReadMP4(r)
		if err != nil { return nil, err }
		return map[string]any{"title": tags.Title}, nil
	case "github.com/guregu/tag":
		metadata, err := guregu.ReadFrom(r)
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title()}, nil
	case "github.com/frolovo22/tag":
		metadata, err := frolovo.ReadMp4(r)
		if err != nil { return nil, err }
		title, err := metadata.GetTitle()
		if err != nil { return nil, err }
		return map[string]any{"title": title}, nil
	case "github.com/rcarmo/go-264/audio/mp4":
		file, err := rcarmo.Open(context.Background(), r, int64(len(data)), rcarmo.Limits{})
		if err != nil { return nil, err }
		return map[string]any{"tracks": len(file.Tracks())}, nil
	case "github.com/edgeware/mp4ff/mp4":
		file, err := edgeware.DecodeFile(r)
		if err != nil { return nil, err }
		if file.Ftyp == nil || file.Moov == nil { return nil, fmt.Errorf("missing ftyp or moov") }
		return map[string]any{"brand": file.Ftyp.MajorBrand(), "tracks": len(file.Moov.Traks)}, nil
	case "github.com/eluv-io/mp4ff/mp4":
		file, err := eluv.DecodeFile(r)
		if err != nil { return nil, err }
		if file.Ftyp == nil || file.Moov == nil { return nil, fmt.Errorf("missing ftyp or moov") }
		return map[string]any{"brand": file.Ftyp.MajorBrand(), "tracks": len(file.Moov.Traks)}, nil
	case "github.com/montybay/mp4ff/mp4":
		file, err := montybay.DecodeFile(r)
		if err != nil { return nil, err }
		if file.Ftyp == nil || file.Moov == nil { return nil, fmt.Errorf("missing ftyp or moov") }
		return map[string]any{"brand": file.Ftyp.MajorBrand(), "tracks": len(file.Moov.Traks)}, nil
	case "github.com/abema/go-mp4":
		boxes, err := abema.ExtractBox(r, nil, abema.BoxPath{abema.BoxTypeMoov()})
		if err != nil { return nil, err }
		if len(boxes) != 1 { return nil, fmt.Errorf("expected one moov box, got %d", len(boxes)) }
		return map[string]any{"moov_size": boxes[0].Size}, nil
	case "github.com/dhowden/tag":
		metadata, err := tag.ReadFrom(r)
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title()}, nil
	case "github.com/Eyevinn/mp4ff/mp4":
		file, err := eyevinn.DecodeFile(r)
		if err != nil { return nil, err }
		if file.Ftyp == nil || file.Moov == nil { return nil, fmt.Errorf("missing ftyp or moov") }
		return map[string]any{"brand": file.Ftyp.MajorBrand(), "tracks": len(file.Moov.Traks)}, nil
	case "github.com/yapingcat/gomedia/go-mp4":
		tracks, err := gomedia.CreateMp4Demuxer(r).ReadHead()
		if err != nil { return nil, err }
		return map[string]any{"tracks": len(tracks)}, nil
	case "github.com/alfg/mp4":
		file, err := alfg.OpenFromBytes(data)
		if err != nil { return nil, err }
		if file.Ftyp == nil { return nil, fmt.Errorf("missing ftyp") }
		return map[string]any{"brand": file.Ftyp.MajorBrand}, nil
	case "github.com/deepch/vdk/format/mp4":
		streams, err := deepch.NewDemuxer(r).Streams()
		if err != nil { return nil, err }
		return map[string]any{"streams": len(streams)}, nil
	case "github.com/jfbus/mp4":
		header, err := jfbus.DecodeHeader(r)
		if err != nil { return nil, err }
		if header.Type != "ftyp" { return nil, fmt.Errorf("expected ftyp, got %s", header.Type) }
		box, err := jfbus.DecodeFtyp(io.LimitReader(r, int64(header.Size)-8))
		if err != nil { return nil, err }
		ftyp, ok := box.(*jfbus.FtypBox)
		if !ok { return nil, fmt.Errorf("ftyp parser returned %T", box) }
		return map[string]any{"brand": ftyp.MajorBrand}, nil
	case "github.com/nareix/joy4/format/mp4":
		streams, err := joy4.NewDemuxer(r).Streams()
		if err != nil { return nil, err }
		return map[string]any{"streams": len(streams)}, nil
	case "github.com/MStoykov/mp4":
		file, err := mstoykov.Decode(rangeReader{data})
		if err != nil { return nil, err }
		if file.Ftyp == nil { return nil, fmt.Errorf("missing ftyp") }
		return map[string]any{"brand": file.Ftyp.MajorBrand}, nil
	case "go4.org/media/heif/bmff":
		box, err := bmff.NewReader(r).ReadAndParseBox(bmff.TypeFtyp)
		if err != nil { return nil, err }
		switch value := box.(type) {
		case *bmff.FileTypeBox:
			return map[string]any{"brand": value.MajorBrand}, nil
		case bmff.FileTypeBox:
			return map[string]any{"brand": value.MajorBrand}, nil
		default:
			return nil, fmt.Errorf("ftyp parser returned %T", box)
		}
	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
}

func main() {
	if len(os.Args) != 3 { panic("usage: go run . PACKAGE CONTROL_PATH") }
	result, err := run(os.Args[1], os.Args[2])
	if err != nil { panic(err) }
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil { panic(err) }
}
