package plyharness
import (
 "encoding/json"
 "fmt"
 "os"
 "reflect"
 "testing"
)
func TestControl(t *testing.T){
 data,err:=os.ReadFile("/input/control");if err!=nil{t.Fatal(err)}
 got,err:=Parse(data);if err!=nil{t.Fatal(err)}
 want:=Result{Vertices:3,Faces:1}
 if !reflect.DeepEqual(got,want){t.Fatalf("control mismatch: got %+v, want %+v",got,want)}
 encoded,err:=json.Marshal(got);if err!=nil{t.Fatal(err)}
 fmt.Printf("OBSERVED_JSON:%s\n",encoded)
}
func FuzzPLY(f *testing.F){f.Fuzz(func(t *testing.T,data []byte){_,_=Parse(data)})}
