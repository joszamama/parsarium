#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <id3v2tag.h>
#include <mpegfile.h>
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 char path[]="/tmp/parsarium-mp3-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);int ok=0;
 {
  TagLib::MPEG::File file(path);
  if(file.isValid()){
   TagLib::ID3v2::Tag *tag=file.ID3v2Tag();
   result->has_id3v2=tag!=nullptr;ok=!tag;
   if(tag){
    std::string title=tag->title().to8Bit(true),artist=tag->artist().to8Bit(true);
    if(title.size()<sizeof(result->title)&&artist.size()<sizeof(result->artist)){
     memcpy(result->title,title.c_str(),title.size()+1);
     memcpy(result->artist,artist.c_str(),artist.size()+1);ok=1;
    }
   }
  }
 }
 unlink(path);return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp3_result result;(void)parsarium_parse_mp3(data,size,&result);return 0;
}
