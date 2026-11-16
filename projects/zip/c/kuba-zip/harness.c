#include "harness.h"
#include <zip.h>
#include <stdlib.h>
#include <string.h>
int parsarium_parse_zip(const uint8_t *data,size_t size,struct parsarium_zip_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 struct zip_t *archive=zip_stream_open((const char *)data,size,0,'r');
 if(!archive)return 0;
 int ok=0;
 ssize_t count=zip_entries_total(archive);
 if(count>0 && zip_entry_openbyindex(archive,0)==0){
  const char *name=zip_entry_name(archive);
  if(name && strlen(name)<sizeof(result->name)){
   result->entries=(size_t)count;result->name_len=strlen(name);memcpy(result->name,name,result->name_len);
   void *content=NULL;size_t length=0;
   ssize_t got=zip_entry_read(archive,&content,&length);
   if(got>=0&&content&&(size_t)got==length&&length<=sizeof(result->content)){
    memcpy(result->content,content,length);result->content_len=length;ok=1;
   }
   free(content);
  }
  zip_entry_close(archive);
 }
 zip_stream_close(archive);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_zip_result r;(void)parsarium_parse_zip(data,size,&r);return 0;}
