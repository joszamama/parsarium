package main
import ("bytes";"image";_ "image/png")
func Parse(data []byte) (map[string]any,error) {
 im,format,e:=image.Decode(bytes.NewReader(data));if e!=nil{return nil,e}
 return map[string]any{"format":format,"width":im.Bounds().Dx(),"height":im.Bounds().Dy()},nil
}
