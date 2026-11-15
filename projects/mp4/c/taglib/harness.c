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
 TagLib_File *file=taglib_file_new(path);
 if(file&&taglib_file_is_valid(file)){
  TagLib_Tag *tag=taglib_file_tag(file);
  const TagLib_AudioProperties *props=taglib_file_audioproperties(file);
  if(tag&&props){char *title=taglib_tag_title(tag);
   if(title&&strlen(title)<sizeof(result->title)){
    strcpy(result->title,title);
    result->duration_seconds=taglib_audioproperties_length(props);ok=1;
   }
  }
 }
 taglib_tag_free_strings();if(file)taglib_file_free(file);
 unlink(path);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp4_result result;(void)parsarium_parse_mp4(data,size,&result);return 0;
}
