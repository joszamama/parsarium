package plyharness
import (
 "bytes"
 polyform "github.com/EliCDavis/polyform/formats/ply"
)
type Result struct {Vertices int `json:"vertices"`; Faces int `json:"faces"`}
func Parse(data []byte)(Result,error){
 mesh,err:=polyform.ReadMesh(bytes.NewReader(data));if err!=nil{return Result{},err}
 return Result{Vertices:mesh.AttributeLength(),Faces:mesh.PrimitiveCount()},nil
}
