#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <mp4file.h>
#include <mp4tag.h>
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 char path[]="/tmp/parsarium-mp4-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);int ok=0;
 result->title=NULL;result->has_duration=0;result->duration_seconds=0;
 {
  TagLib::MP4::File file(path);
  if(file.isValid()){
   ok=1;
   if(file.tag()){
    std::string title=file.tag()->title().to8Bit(true);
    if(!(result->title=strdup(title.c_str())))ok=0;
   }
   if(file.audioProperties()){
    result->has_duration=1;result->duration_seconds=file.audioProperties()->lengthInSeconds();
   }
  }
 }
 unlink(path);return ok;
}
void parsarium_free_mp4(struct parsarium_mp4_result *result){free(result->title);result->title=NULL;}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;if(parsarium_parse_mp4(data,size,&result))parsarium_free_mp4(&result);return 0;
}
