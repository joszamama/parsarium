#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <tag_c.h>
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 char path[]="/tmp/parsarium-mp4-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);int ok=0;
 result->title=NULL;result->has_duration=0;result->duration_seconds=0;
 TagLib_File *file=taglib_file_new(path);
 if(file&&taglib_file_is_valid(file)){
  TagLib_Tag *tag=taglib_file_tag(file);
  const TagLib_AudioProperties *props=taglib_file_audioproperties(file);
  ok=1;
  if(tag){char *title=taglib_tag_title(tag);
   if(title&&!(result->title=strdup(title)))ok=0;
  }
  if(props){result->has_duration=1;result->duration_seconds=taglib_audioproperties_length(props);}
 }
 taglib_tag_free_strings();if(file)taglib_file_free(file);
 unlink(path);return ok;
}
void parsarium_free_mp4(struct parsarium_mp4_result *result){free(result->title);result->title=NULL;}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;if(parsarium_parse_mp4(data,size,&result))parsarium_free_mp4(&result);return 0;
}
