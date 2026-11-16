#include "harness.h"
#include <unarr.h>
#include <string.h>
int parsarium_parse_zip(const uint8_t *data,size_t size,struct parsarium_zip_result *result) {
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 ar_stream *stream=ar_open_memory(data,size);if(!stream)return 0;
 ar_archive *archive=ar_open_zip_archive(stream,false);if(!archive){ar_close(stream);return 0;}
 int ok=0;
 if(ar_parse_entry(archive)) {
  const char *entry_name=ar_entry_get_name(archive);
  size_t content_size=ar_entry_get_size(archive);
  if(entry_name && content_size<=sizeof(result->content)) {
   size_t name_len=strlen(entry_name);
   if(name_len>0 && name_len<sizeof(result->name)) {
    memcpy(result->name,entry_name,name_len);result->name_len=name_len;
    if(ar_entry_uncompress(archive,result->content,content_size)) {
     result->content_len=content_size;result->entries=1;
     while(ar_parse_entry(archive))++result->entries;
     ok=ar_at_eof(archive);
    }
   }
  }
 }
 ar_close_archive(archive);ar_close(stream);
 return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_zip_result result;(void)parsarium_parse_zip(data,size,&result);return 0;
}
