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
static int read_dimension(const Exiv2::XmpData &xmp,const char *key,long *out){
 auto it=xmp.findKey(Exiv2::XmpKey(key));if(it==xmp.end())return 0;
 std::string text=it->toString();char *end=nullptr;long value=strtol(text.c_str(),&end,10);
 if(text.empty()||*end||value<=0||value>65535)return 0;
 *out=value;return 1;
}
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 Exiv2::LogMsg::setLevel(Exiv2::LogMsg::mute);
 char path[]="/tmp/parsarium-mp4-XXXXXX.mp4";int fd=mkstemps(path,4);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);int ok=0;
 try{
  auto image=Exiv2::ImageFactory::open(path);
  if(image&&image->imageType()==Exiv2::ImageType::qtime){
   image->readMetadata();
   const Exiv2::XmpData &xmp=image->xmpData();
   auto brand=xmp.findKey(Exiv2::XmpKey("Xmp.video.MajorBrand"));
   if(brand!=xmp.end()&&read_dimension(xmp,"Xmp.video.Width",&result->width)
      &&read_dimension(xmp,"Xmp.video.Height",&result->height)){
    std::string name=brand_name(brand->toString());
    if(!name.empty()&&name.size()<sizeof(result->brand)
       &&name.find_first_of("\"\\")==std::string::npos){
     memcpy(result->brand,name.c_str(),name.size()+1);ok=1;
    }
   }
  }
 }catch(const std::exception &){ok=0;}
 unlink(path);return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;(void)parsarium_parse_mp4(data,size,&result);return 0;
}
