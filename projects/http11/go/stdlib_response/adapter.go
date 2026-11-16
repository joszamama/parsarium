package main
import ("bufio";"bytes";"io";"net/http")
func Parse(data []byte) (map[string]any,error) {
 r,e:=http.ReadResponse(bufio.NewReader(bytes.NewReader(data)),&http.Request{Method:"GET"});if e!=nil{return nil,e};defer r.Body.Close()
 b,e:=io.ReadAll(r.Body);if e!=nil{return nil,e}
 return map[string]any{"status":r.StatusCode,"proto":r.Proto,"body":string(b)},nil
}
