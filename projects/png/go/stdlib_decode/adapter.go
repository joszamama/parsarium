package main
import ("bytes";"image/color";"image/png")
func Parse(data []byte) (map[string]any,error) {
 im,e:=png.Decode(bytes.NewReader(data));if e!=nil{return nil,e}
 a:=color.NRGBAModel.Convert(im.At(0,0)).(color.NRGBA);b:=color.NRGBAModel.Convert(im.At(1,0)).(color.NRGBA)
 return map[string]any{"width":im.Bounds().Dx(),"height":im.Bounds().Dy(),"rgba":[]int{int(a.R),int(a.G),int(a.B),int(a.A),int(b.R),int(b.G),int(b.B),int(b.A)}},nil
}
