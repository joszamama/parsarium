package main
import ("archive/zip";"io";"os")
func Parse(data []byte) (any,error) {
 f,e:=os.CreateTemp("","parsarium-zip-*.zip");if e!=nil{return nil,e};defer os.Remove(f.Name())
 if _,e=f.Write(data);e!=nil{f.Close();return nil,e};if e=f.Close();e!=nil{return nil,e}
 z,e:=zip.OpenReader(f.Name());if e!=nil{return nil,e};defer z.Close()
 entries:=[]map[string]any{}
 for _,file:=range z.File{
  r,e:=file.Open();if e!=nil{return nil,e}
  b,e:=io.ReadAll(r);r.Close();if e!=nil{return nil,e}
  entries=append(entries,map[string]any{"name":file.Name,"text":string(b)})
 }
 if len(entries)==1{return entries[0],nil}
 return entries,nil
}
