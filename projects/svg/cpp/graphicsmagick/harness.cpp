#include "harness.h"
#include <Magick++.h>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <unistd.h>
int parsarium_parse_svg(const uint8_t*data,size_t size,struct parsarium_svg_result*result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 char path[]="/tmp/parsarium-svg-XXXXXX.svg";int fd=mkstemps(path,4);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}close(fd);
 int ok=0;
 try{
  Magick::InitializeMagick(nullptr);
  Magick::Image image{std::string(path)};
  if(image.columns()==2&&image.rows()==1){
   Magick::ColorRGB a(image.pixelColor(0,0)),b(image.pixelColor(1,0));
   result->width=2;result->height=1;
   result->first[0]=std::lround(a.red()*255);result->first[1]=std::lround(a.green()*255);result->first[2]=std::lround(a.blue()*255);
   result->second[0]=std::lround(b.red()*255);result->second[1]=std::lround(b.green()*255);result->second[2]=std::lround(b.blue()*255);
   ok=1;
  }
 }catch(const std::exception&){}
 unlink(path);return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t*data,size_t size){struct parsarium_svg_result r;(void)parsarium_parse_svg(data,size,&r);return 0;}
