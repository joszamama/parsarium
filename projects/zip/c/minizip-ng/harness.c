#include "harness.h"
#include <mz.h>
#include <mz_strm.h>
#include <mz_zip.h>
#include <mz_zip_rw.h>
#include <string.h>
int parsarium_parse_zip(const uint8_t *data,size_t size,struct parsarium_zip_result *result) {
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 void *archive=mz_zip_reader_create();if(!archive)return 0;
 int ok=0;
 mz_zip_file *info=NULL;
 if(mz_zip_reader_open_buffer(archive,data,(int32_t)size,1)!=MZ_OK)goto done;
 if(mz_zip_reader_goto_first_entry(archive)!=MZ_OK)goto done;
 if(mz_zip_reader_entry_get_info(archive,&info)!=MZ_OK || !info || !info->filename || info->uncompressed_size>sizeof(result->content))goto done;
 result->name_len=strlen(info->filename);
 if(!result->name_len||result->name_len>=sizeof(result->name))goto done;
 memcpy(result->name,info->filename,result->name_len);
 if(mz_zip_reader_entry_open(archive)!=MZ_OK)goto done;
 {
  int32_t n=mz_zip_reader_entry_read(archive,result->content,sizeof(result->content));
  int32_t closed=mz_zip_reader_entry_close(archive);
  if(n<0 || n!=info->uncompressed_size || closed!=MZ_OK)goto done;
  result->content_len=(size_t)n;
 }
 result->entries=1;
 while(mz_zip_reader_goto_next_entry(archive)==MZ_OK)++result->entries;
 ok=1;
done:
 mz_zip_reader_close(archive);mz_zip_reader_delete(&archive);
 return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_zip_result result;(void)parsarium_parse_zip(data,size,&result);return 0;
}
