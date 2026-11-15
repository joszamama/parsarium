package pdfharness
import (
 "bytes"
 "fmt"
 pdf "github.com/ledongthuc/pdf"
)
type Result struct {Pages int `json:"pages"`}
func Parse(data []byte)(Result,error){
 if len(data)==0 || len(data)>(1<<20){return Result{},fmt.Errorf("input outside harness limit")}
 doc,err:=pdf.NewReader(bytes.NewReader(data),int64(len(data)))
 if err!=nil{return Result{},err}
 return Result{Pages:doc.NumPage()},nil
}
