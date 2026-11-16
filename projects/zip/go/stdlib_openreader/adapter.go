package main
import ("archive/zip";"io";"os")
func Parse(data []byte) (map[string]any,error) {
 f,e:=os.CreateTemp("","parsarium-zip-*.zip");if e!=nil{return nil,e};defer os.Remove(f.Name())
 if _,e=f.Write(data);e!=nil{f.Close();return nil,e};if e=f.Close();e!=nil{return nil,e}
 z,e:=zip.OpenReader(f.Name());if e!=nil{return nil,e};defer z.Close()
 if len(z.File)!=1{return nil,io.ErrUnexpectedEOF};r,e:=z.File[0].Open();if e!=nil{return nil,e};defer r.Close()
 b,e:=io.ReadAll(r);if e!=nil{return nil,e}
 return map[string]any{"name":z.File[0].Name,"text":string(b)},nil
}
