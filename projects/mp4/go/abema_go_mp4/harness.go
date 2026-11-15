package mp4harness
import (
 "bytes"
 "fmt"
 mp4 "github.com/abema/go-mp4"
)
type Result struct {MoovSize uint64 `json:"moov_size"`}
func Parse(data []byte)(Result,error){
 if len(data)==0 || len(data)>(1<<20){return Result{},fmt.Errorf("input outside harness limit")}
 boxes,err:=mp4.ExtractBox(bytes.NewReader(data),nil,mp4.BoxPath{mp4.BoxTypeMoov()})
 if err!=nil{return Result{},err}
 if len(boxes)!=1{return Result{},fmt.Errorf("expected one moov box")}
 return Result{MoovSize:boxes[0].Size},nil
}
