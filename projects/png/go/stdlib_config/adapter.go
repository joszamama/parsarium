package main
import ("bytes";"image/png")
func Parse(data []byte) (map[string]any,error) {
 cfg,e:=png.DecodeConfig(bytes.NewReader(data));if e!=nil{return nil,e}
 return map[string]any{"width":cfg.Width,"height":cfg.Height},nil
}
