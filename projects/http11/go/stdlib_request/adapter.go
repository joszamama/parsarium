package main
import ("bufio";"bytes";"net/http")
func Parse(data []byte) (map[string]any,error) {
 r,e:=http.ReadRequest(bufio.NewReader(bytes.NewReader(data)));if e!=nil{return nil,e};defer r.Body.Close()
 return map[string]any{"host":r.Host,"method":r.Method,"proto":r.Proto,"target":r.URL.RequestURI()},nil
}
