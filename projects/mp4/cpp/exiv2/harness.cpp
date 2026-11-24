#include "harness.h"
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <exception>
#include <string>
#include <exiv2/exiv2.hpp>
// Exiv2 labels the major brand with a version suffix, e.g.
// "MP4 Base Media v1 [IS0 14496-12:2003]". Report the brand name only.
static std::string brand_name(std::string label){
 size_t cut=label.find(" [");if(cut!=std::string::npos)label.erase(cut);
 cut=label.rfind(" v");
 if(cut!=std::string::npos&&cut+2<label.size()&&label.find_first_not_of("0123456789",cut+2)==std::string::npos)label.erase(cut);
 return label;
}
// A dimension is reported only when Exiv2 recorded it as an integer; an audio-only
// file has no video track, so Exiv2 records no width or height. width/height are the
// coded frame size from the visual sample description (Xmp.video.SourceImageWidth/
// SourceImageHeight); Xmp.video.Width/Height hold the tkhd presentation size, which a
// file may set differently.
static int read_dimension(const Exiv2::XmpData &xmp,const char *key,long *out){
 auto it=xmp.findKey(Exiv2::XmpKey(key));if(it==xmp.end())return 0;
 std::string text=it->toString();char *end=nullptr;long value=strtol(text.c_str(),&end,10);
 if(text.empty()||*end)return 0;
 *out=value;return 1;
}
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result){
 if(!result)return 0;
 result->has_brand=result->has_width=result->has_height=0;result->brand.clear();result->error.clear();
 if(!data||!size||size>(1u<<20)){result->error="input outside harness limit";return 0;}
 Exiv2::LogMsg::setLevel(Exiv2::LogMsg::mute);
 char path[]="/tmp/parsarium-mp4-XXXXXX.mp4";int fd=mkstemps(path,4);
 if(fd<0){result->error="cannot create parser input";return 0;}
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);
  if(n<=0){close(fd);unlink(path);result->error="cannot write parser input";return 0;}off+=(size_t)n;}
 close(fd);int ok=0;
 try{
  auto image=Exiv2::ImageFactory::open(path);
  if(!image)result->error="Exiv2::ImageFactory::open returned no image";
  else if(image->imageType()!=Exiv2::ImageType::qtime)
   result->error="Exiv2 did not open the file as QuickTime (image type "+std::to_string((int)image->imageType())+")";
  else{
   image->readMetadata();
   const Exiv2::XmpData &xmp=image->xmpData();
   auto brand=xmp.findKey(Exiv2::XmpKey("Xmp.video.MajorBrand"));
   if(brand!=xmp.end()){result->brand=brand_name(brand->toString());result->has_brand=1;}
   result->has_width=read_dimension(xmp,"Xmp.video.SourceImageWidth",&result->width);
   result->has_height=read_dimension(xmp,"Xmp.video.SourceImageHeight",&result->height);
   ok=1;
  }
 }catch(const std::exception &error){result->error=error.what();ok=0;}
 unlink(path);return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;(void)parsarium_parse_mp4(data,size,&result);return 0;
}
