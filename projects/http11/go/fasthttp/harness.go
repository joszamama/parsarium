package httpharness

import (
    "bufio"
    "bytes"
    "fmt"
    "github.com/valyala/fasthttp"
)

type Result struct {
    Method string `json:"method"`
    Target string `json:"target"`
    Host string `json:"host"`
}
func Parse(data []byte) (Result, error) {
    if len(data)==0 || len(data)>(1<<20) { return Result{}, fmt.Errorf("input outside harness limit") }
    var request fasthttp.Request
    if err:=request.Read(bufio.NewReader(bytes.NewReader(data))); err!=nil { return Result{}, err }
    return Result{Method:string(request.Header.Method()),Target:string(request.RequestURI()),Host:string(request.Host())},nil
}
