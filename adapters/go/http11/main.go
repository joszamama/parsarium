// Run one pinned Go HTTP/1.1 message parser against a local wire control.
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strings"

	oohttp "github.com/FastTLS/oohttp"
	fiohttp "github.com/antlabs/fio/http"
	"github.com/antlabs/httparser"
	"github.com/cloudwego/hertz/pkg/protocol"
	hertzreq "github.com/cloudwego/hertz/pkg/protocol/http1/req"
	"github.com/evanphx/wildcat"
	oldfast "github.com/go-fasthttp/fasthttp"
	"github.com/gobwas/httphead"
	spindrift "github.com/hellpuffyt/spindrift/http1"
	httpport "github.com/hsiafan/httpdump/httpport"
	blaze "github.com/justIliane/blazehttp/pkg/header"
	"github.com/lemon4ksan/foundation/silicon/bytesconv"
	"github.com/lemon4ksan/mach/server/h1"
	fib "github.com/lesismal/fib/http"
	"github.com/lesismal/nbio/nbhttp"
	metarpc "github.com/meta-apex/metarpc/codec/http"
	"github.com/nelthaarion/breeze"
	"github.com/openctemio/openctem/api/pkg/domain/evidence"
	nucleiraw "github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw"
	simd "github.com/sebishogun/simdhttp/http1"
	"github.com/valyala/fasthttp"
	clashhttp "github.com/zhaofenghao/clash/listener/http"
	gnalloyhttp1 "gnalloy.org/codec-http1"
	gnbuffer "gnalloy.org/gnalloy/buffer"
)

type byteReader struct {
	data   []byte
	offset int
}

type capturedHTTP struct {
	nbhttp.Processor
	method, target, proto string
	complete              bool
}

func (c *capturedHTTP) OnMethod(_ *nbhttp.Parser, method string)     { c.method = method }
func (c *capturedHTTP) OnURL(_ *nbhttp.Parser, target string) error  { c.target = target; return nil }
func (c *capturedHTTP) OnProto(_ *nbhttp.Parser, proto string) error { c.proto = proto; return nil }
func (c *capturedHTTP) OnComplete(_ *nbhttp.Parser)                  { c.complete = true }

func (r *byteReader) Peek(n int) ([]byte, error) {
	if n < 0 || r.offset+n > len(r.data) {
		return nil, io.EOF
	}
	return r.data[r.offset : r.offset+n], nil
}
func (r *byteReader) Skip(n int) error {
	if n < 0 || r.offset+n > len(r.data) {
		return io.EOF
	}
	r.offset += n
	return nil
}
func (r *byteReader) Release() error { return nil }
func (r *byteReader) Len() int       { return len(r.data) - r.offset }
func (r *byteReader) ReadByte() (byte, error) {
	b, err := r.Peek(1)
	if err != nil {
		return 0, err
	}
	r.offset++
	return b[0], nil
}
func (r *byteReader) ReadBinary(n int) ([]byte, error) {
	b, err := r.Peek(n)
	if err != nil {
		return nil, err
	}
	r.offset += n
	return append([]byte(nil), b...), nil
}

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	switch name {
	case "github.com/nelthaarion/breeze":
		request, _, err := breeze.ParseHTTPRequest(data)
		if err != nil {
			return nil, err
		}
		if request == nil {
			return nil, fmt.Errorf("HTTP request not completed")
		}
		target := request.Path
		if len(request.Query) > 0 {
			target += "?" + request.Query.Encode()
		}
		var host string
		for key, value := range request.Header {
			if strings.EqualFold(key, "Host") {
				host = value
			}
		}
		return map[string]any{"method": string(request.Method), "target": target, "host": host}, nil
	case "github.com/lemon4ksan/mach/server/h1":
		var request h1.Request
		var buffer bytesconv.ByteBuffer
		if err := request.ReadRequest(bufio.NewReader(bytes.NewReader(data)), &buffer, 1<<20); err != nil {
			return nil, err
		}
		return map[string]any{"method": request.Method, "target": request.URI, "host": request.Host, "proto": request.Proto}, nil
	case "github.com/antlabs/httparser":
		parser := httparser.New(httparser.REQUEST)
		var target string
		complete := false
		setting := httparser.Setting{URL: func(_ *httparser.Parser, b []byte, _ int) { target += string(b) }, MessageComplete: func(_ *httparser.Parser, _ int) { complete = true }}
		if _, err := parser.Execute(&setting, data); err != nil {
			return nil, err
		}
		if !complete {
			return nil, fmt.Errorf("HTTP request not completed")
		}
		return map[string]any{"method": parser.Method.String(), "target": target, "major": parser.Major, "minor": parser.Minor}, nil
	case "github.com/hsiafan/httpdump/httpport":
		request, err := httpport.ReadRequest(bufio.NewReader(bytes.NewReader(data)))
		if err != nil {
			return nil, err
		}
		defer request.Body.Close()
		return map[string]any{"method": request.Method, "target": request.RequestURI, "host": request.Host, "proto": request.Proto}, nil
	case "github.com/openctemio/openctem/api/pkg/domain/evidence":
		request := evidence.ParseRawRequest(string(data), "http://example.test")
		return map[string]any{"method": request.Method, "url": request.URL, "proto": request.HTTPVersion}, nil
	case "github.com/go-fasthttp/fasthttp":
		var request oldfast.Request
		if err := request.Read(bufio.NewReader(bytes.NewReader(data))); err != nil {
			return nil, err
		}
		return map[string]any{"method": string(request.Header.Method()), "target": string(request.RequestURI()), "host": string(request.Host())}, nil
	case "github.com/zhaofenghao/clash/listener/http":
		request, err := clashhttp.ReadRequest(bufio.NewReader(bytes.NewReader(data)))
		if err != nil {
			return nil, err
		}
		defer request.Body.Close()
		return map[string]any{"method": request.Method, "target": request.RequestURI, "host": request.Host, "proto": request.Proto}, nil
	case "github.com/antlabs/fio/http":
		parser := fiohttp.NewParser(0)
		if _, err := parser.Parse(data); err != nil {
			return nil, err
		}
		if !parser.Done() {
			return nil, fmt.Errorf("HTTP request not completed")
		}
		request := parser.Request()
		return map[string]any{"method": request.Method, "target": request.Target, "proto": request.Proto}, nil
	case "github.com/meta-apex/metarpc/codec/http":
		parser := metarpc.NewParser(true)
		defer parser.Release()
		_, complete, err := parser.Parse(data)
		if err != nil {
			return nil, err
		}
		if !complete {
			return nil, fmt.Errorf("HTTP request not completed")
		}
		request := parser.GetRequest()
		return map[string]any{"method": request.MethodString(), "target": string(request.RequestURI()), "host": request.HostString()}, nil
	case "github.com/lesismal/fib/http":
		parser := fib.NewParser(fib.Config{})
		requests, err := parser.Feed(data)
		if err != nil {
			return nil, err
		}
		if len(requests) != 1 {
			return nil, fmt.Errorf("expected one request, got %d", len(requests))
		}
		request := requests[0]
		return map[string]any{"method": request.Method, "target": request.RequestURI, "host": request.Host, "proto": request.Proto}, nil
	case "github.com/lesismal/nbio/nbhttp":
		capture := &capturedHTTP{Processor: nbhttp.NewEmptyProcessor()}
		parser := nbhttp.NewParser(nil, &nbhttp.Engine{}, capture, false, nil)
		if err := parser.Parse(data); err != nil {
			return nil, err
		}
		if !capture.complete {
			return nil, fmt.Errorf("HTTP request not completed")
		}
		return map[string]any{"method": capture.method, "target": capture.target, "proto": capture.proto}, nil
	case "github.com/gobwas/httphead":
		end := bytes.Index(data, []byte("\r\n"))
		if end < 0 {
			return nil, fmt.Errorf("no request line")
		}
		line, ok := httphead.ParseRequestLine(data[:end])
		if !ok {
			return nil, fmt.Errorf("request line parse failed")
		}
		return map[string]any{"method": string(line.Method), "target": string(line.URI), "major": line.Version.Major, "minor": line.Version.Minor}, nil
	case "github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw":
		request, err := nucleiraw.ParseRawRequest(string(data), false)
		if err != nil {
			return nil, err
		}
		return map[string]any{"method": request.Method, "target": request.Path, "host": request.Headers["Host"]}, nil
	case "gnalloy.org/codec-http1":
		decoder, err := gnalloyhttp1.NewRequestDecoder(1<<20, 1<<20)
		if err != nil {
			return nil, err
		}
		source := gnbuffer.NewHeapBuffer(len(data))
		if _, err := source.WriteBytes(data); err != nil {
			return nil, err
		}
		input := gnbuffer.NewCompositeByteBuf()
		input.Append(source)
		defer input.Release()
		message, err := decoder.Decode(nil, input)
		if err != nil {
			return nil, err
		}
		request, ok := message.(*gnalloyhttp1.Request)
		if !ok || request == nil {
			return nil, fmt.Errorf("HTTP request not completed")
		}
		defer request.Release()
		return map[string]any{"method": strings.Clone(request.Method), "target": strings.Clone(request.URI), "host": strings.Clone(request.Headers.Get("Host")), "proto": strings.Clone(request.Version)}, nil
	case "github.com/cloudwego/hertz/pkg/protocol/http1/req":
		var request protocol.Request
		if err := hertzreq.Read(&request, &byteReader{data: data}); err != nil {
			return nil, err
		}
		return map[string]any{"method": string(request.Method()), "target": string(request.RequestURI()), "host": string(request.Host())}, nil
	case "github.com/FastTLS/oohttp":
		request, err := oohttp.ReadRequest(bufio.NewReader(bytes.NewReader(data)))
		if err != nil {
			return nil, err
		}
		defer request.Body.Close()
		return map[string]any{"method": request.Method, "target": request.RequestURI, "host": request.Host, "proto": request.Proto}, nil
	case "github.com/hellpuffyt/spindrift/http1":
		request, err := spindrift.ReadRequest(bufio.NewReader(bytes.NewReader(data)), spindrift.Limits{})
		if err != nil {
			return nil, err
		}
		return map[string]any{"method": request.Method, "target": request.Target, "proto": request.Proto()}, nil
	case "github.com/justIliane/blazehttp/pkg/header":
		var request blaze.ParsedRequest
		if _, err := blaze.Parse(data, &request); err != nil {
			return nil, err
		}
		return map[string]any{"method": string(request.Method), "target": string(request.URI), "proto": string(request.Version), "host": string(request.HeaderValue([]byte("Host")))}, nil
	case "github.com/valyala/fasthttp":
		var request fasthttp.Request
		if err := request.Read(bufio.NewReader(bytes.NewReader(data))); err != nil {
			return nil, err
		}
		return map[string]any{"method": string(request.Header.Method()), "target": string(request.RequestURI()), "host": string(request.Host())}, nil
	case "github.com/evanphx/wildcat":
		parser := wildcat.NewHTTPParser()
		if _, err := parser.Parse(data); err != nil {
			return nil, err
		}
		return map[string]any{"method": string(parser.Method), "target": string(parser.Path), "proto": string(parser.Version), "host": string(parser.Host())}, nil
	case "github.com/sebishogun/simdhttp/http1":
		var request simd.Request
		if _, err := simd.Parse(&request, data, simd.Compatible); err != nil {
			return nil, err
		}
		return map[string]any{"method": string(request.Method), "target": string(request.Target), "proto": string(request.Proto)}, nil
	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
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
