// Run one pinned Go MP3 or ID3v2 parser against the valid tagged MP3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"

	dece "github.com/dece2183/go-stream-mp3"
	faiface "github.com/faiface/beep/mp3"
	fgergo "github.com/fgergo/mp3"
	gopxl "github.com/gopxl/beep/v2/mp3"
	ebiten "github.com/hajimehoshi/ebiten/v2/audio/mp3"
	hajime "github.com/hajimehoshi/go-mp3"
	mattetti "github.com/mattetti/audio/mp3"
	qiniu "github.com/qiniu/audio/mp3"
	"github.com/sa6mwa/mp3duration"
	tcolgate "github.com/tcolgate/mp3"
	"github.com/tosone/minimp3"
	bogem "github.com/bogem/id3v2/v2"
	"github.com/dhowden/tag"
	frolovo "github.com/frolovo22/tag"
	"github.com/gcottom/mp3meta"
	guregu "github.com/guregu/tag"
	icanhaz "github.com/icanhazbroccoli/tag"
	ascherkus "github.com/ascherkus/go-id3/src/id3"
	dustin "github.com/dustin/go-id3"
	"honnef.co/go/id3"
)

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil { return nil, err }
	r := bytes.NewReader(data)
	switch name {
	case "github.com/faiface/beep/mp3":
		stream, format, err := faiface.Decode(io.NopCloser(r))
		if err != nil { return nil, err }
		defer stream.Close()
		samples := make([][2]float64, 16)
		n, ok := stream.Stream(samples)
		if !ok && n == 0 { return nil, fmt.Errorf("no decoded samples") }
		return map[string]any{"sample_rate": int(format.SampleRate), "samples": n}, nil
	case "github.com/gopxl/beep/v2/mp3":
		stream, format, err := gopxl.Decode(io.NopCloser(r))
		if err != nil { return nil, err }
		defer stream.Close()
		samples := make([][2]float64, 16)
		n, ok := stream.Stream(samples)
		if !ok && n == 0 { return nil, fmt.Errorf("no decoded samples") }
		return map[string]any{"sample_rate": int(format.SampleRate), "samples": n}, nil
	case "github.com/hajimehoshi/go-mp3":
		decoder, err := hajime.NewDecoder(r)
		if err != nil { return nil, err }
		buf := make([]byte, 64)
		n, err := decoder.Read(buf)
		if err != nil && err != io.EOF { return nil, err }
		return map[string]any{"sample_rate": decoder.SampleRate(), "decoded_bytes": n}, nil
	case "github.com/hajimehoshi/ebiten/v2/audio/mp3":
		decoder, err := ebiten.DecodeWithoutResampling(r)
		if err != nil { return nil, err }
		buf := make([]byte, 64)
		n, err := decoder.Read(buf)
		if err != nil && err != io.EOF { return nil, err }
		return map[string]any{"sample_rate": decoder.SampleRate(), "decoded_bytes": n}, nil
	case "github.com/dece2183/go-stream-mp3":
		decoder, err := dece.NewDecoder(r)
		if err != nil { return nil, err }
		buf := make([]byte, 64)
		n, err := decoder.Read(buf)
		if err != nil && err != io.EOF { return nil, err }
		return map[string]any{"sample_rate": decoder.SampleRate(), "decoded_bytes": n}, nil
	case "github.com/tcolgate/mp3":
		decoder := tcolgate.NewDecoder(r)
		var frame tcolgate.Frame
		var skipped int
		if err := decoder.Decode(&frame, &skipped); err != nil { return nil, err }
		return map[string]any{"samples": frame.Samples(), "frame_bytes": frame.Size()}, nil
	case "github.com/fgergo/mp3":
		decoder := fgergo.NewDecoder(r)
		var frame fgergo.Frame
		var skipped int
		if err := decoder.Decode(&frame, &skipped); err != nil { return nil, err }
		return map[string]any{"samples": frame.Samples(), "frame_bytes": frame.Size()}, nil
	case "github.com/tosone/minimp3":
		decoder, decoded, err := minimp3.DecodeFull(data)
		if err != nil { return nil, err }
		defer decoder.Close()
		return map[string]any{"sample_rate": decoder.SampleRate, "channels": decoder.Channels, "decoded_bytes": len(decoded)}, nil
	case "github.com/sa6mwa/mp3duration":
		info, err := mp3duration.ReadFile(path)
		if err != nil { return nil, err }
		return map[string]any{"frames": info.Frames, "duration_ms": info.TimeDuration.Milliseconds()}, nil
	case "github.com/mattetti/audio/mp3":
		decoder := mattetti.NewDecoder(r)
		duration, err := decoder.Duration()
		if err != nil { return nil, err }
		return map[string]any{"duration_ms": duration.Milliseconds(), "frames": decoder.NbrFrames}, nil
	case "github.com/qiniu/audio/mp3":
		decoded, err := qiniu.Decode(r)
		if err != nil { return nil, err }
		buf := make([]byte, 64)
		n, err := decoded.Read(buf)
		if err != nil && err != io.EOF { return nil, err }
		return map[string]any{"sample_rate": decoded.SampleRate(), "channels": decoded.Channels(), "decoded_bytes": n}, nil
	case "github.com/bogem/id3v2/v2":
		metadata, err := bogem.ParseReader(r, bogem.Options{Parse: true})
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title()}, nil
	case "github.com/dhowden/tag":
		metadata, err := tag.ReadFrom(r)
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title()}, nil
	case "github.com/gcottom/mp3meta":
		metadata, err := mp3meta.ParseMP3(r)
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title}, nil
	case "github.com/guregu/tag":
		metadata, err := guregu.ReadFrom(r)
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title()}, nil
	case "github.com/icanhazbroccoli/tag":
		metadata, err := icanhaz.ReadFrom(r)
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title()}, nil
	case "github.com/frolovo22/tag":
		metadata, err := frolovo.ReadID3v23(r)
		if err != nil { return nil, err }
		title, err := metadata.GetTitle()
		if err != nil { return nil, err }
		return map[string]any{"title": title}, nil
	case "github.com/ascherkus/go-id3/src/id3":
		metadata := ascherkus.Read(r)
		if metadata == nil { return nil, fmt.Errorf("no ID3v2 metadata") }
		return map[string]any{"title": metadata.Name}, nil
	case "github.com/dustin/go-id3":
		metadata := dustin.Read(r)
		if metadata == nil { return nil, fmt.Errorf("no ID3v2 metadata") }
		return map[string]any{"title": metadata.Name}, nil
	case "honnef.co/go/id3":
		metadata, err := id3.NewDecoder(r).Parse()
		if err != nil { return nil, err }
		return map[string]any{"title": metadata.Title()}, nil
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
