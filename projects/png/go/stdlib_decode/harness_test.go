package main
import ("encoding/json";"fmt";"os";"reflect";"testing")
const expectedJSON = "{\"height\": 1, \"rgba\": [255, 0, 0, 255, 0, 255, 0, 255], \"width\": 2}"
func TestControl(t *testing.T) {
 data,e:=os.ReadFile("/input/control");if e!=nil{t.Fatal(e)}
 got,e:=Parse(data);if e!=nil{t.Fatal(e)}
 var want map[string]any;if e=json.Unmarshal([]byte(expectedJSON),&want);e!=nil{t.Fatal(e)}
 var normalized map[string]any;b,_:=json.Marshal(got);if e=json.Unmarshal(b,&normalized);e!=nil{t.Fatal(e)}
 if !reflect.DeepEqual(normalized,want){t.Fatalf("control mismatch: %s",b)}
 fmt.Printf("OBSERVED_JSON:%s\n",b)
}
func FuzzParser(f *testing.F){f.Fuzz(func(t *testing.T,data []byte){if len(data)>0&&len(data)<(1<<20){_,_=Parse(data)}})}
