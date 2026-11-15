#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <tag_c.h>
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 char path[]="/tmp/parsarium-mp3-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);int ok=0;
 TagLib_File *file=taglib_file_new_type(path,TagLib_File_MPEG);
 if(file&&taglib_file_is_valid(file)){
  TagLib_Tag *tag=taglib_file_tag(file);
  if(tag){char *title=taglib_tag_title(tag),*artist=taglib_tag_artist(tag);
   if(title&&artist&&strlen(title)<sizeof(result->title)&&strlen(artist)<sizeof(result->artist)){
    strcpy(result->title,title);strcpy(result->artist,artist);ok=1;
   }
  }
 }
 taglib_tag_free_strings();if(file)taglib_file_free(file);
 unlink(path);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp3_result result;(void)parsarium_parse_mp3(data,size,&result);return 0;
}
