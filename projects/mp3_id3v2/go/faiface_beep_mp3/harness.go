package mp3harness
import (
 "bytes"
 "fmt"
 "io"
 mp3 "github.com/faiface/beep/mp3"
)
type Result struct {SampleRate int `json:"sample_rate"`; Samples int `json:"samples"`}
func Parse(data []byte)(Result,error){
 stream,format,err:=mp3.Decode(io.NopCloser(bytes.NewReader(data)));if err!=nil{return Result{},err}
 defer stream.Close()
 samples:=make([][2]float64,16)
 n,ok:=stream.Stream(samples);if !ok&&n==0{return Result{},fmt.Errorf("no decoded samples")}
 return Result{SampleRate:int(format.SampleRate),Samples:n},nil
}
