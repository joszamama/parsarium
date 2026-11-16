#include "harness.h"
#include <physfs.h>
#include <string.h>
int parsarium_parse_zip(const uint8_t *data,size_t size,struct parsarium_zip_result *result) {
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 if(!PHYSFS_init("parsarium"))return 0;
 int ok=0;
 if(PHYSFS_mountMemory(data,size,NULL,"input.zip",NULL,1)) {
  char **names=PHYSFS_enumerateFiles("/");
  if(names) {
   size_t count=0;while(names[count])++count;
   if(count && strlen(names[0])<sizeof(result->name)) {
    PHYSFS_File *file=PHYSFS_openRead(names[0]);
    if(file) {
     PHYSFS_sint64 length=PHYSFS_fileLength(file);
     if(length>=0 && length<=(PHYSFS_sint64)sizeof(result->content) &&
        PHYSFS_readBytes(file,result->content,(PHYSFS_uint64)length)==length) {
      result->entries=count;result->name_len=strlen(names[0]);
      memcpy(result->name,names[0],result->name_len);
      result->content_len=(size_t)length;ok=1;
     }
     PHYSFS_close(file);
    }
   }
   PHYSFS_freeList(names);
  }
 }
 PHYSFS_deinit();return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_zip_result result;(void)parsarium_parse_zip(data,size,&result);return 0;
}
