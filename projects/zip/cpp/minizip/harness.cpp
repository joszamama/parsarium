#include "harness.h"
#include <minizip/unzip.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
int parsarium_parse_zip(const uint8_t *data,size_t size,struct parsarium_zip_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));char path[]="/tmp/parsarium-minizip-XXXXXX";
 int fd=mkstemp(path);if(fd<0)return 0;
 ssize_t written=write(fd,data,size);close(fd);
 if(written<0||(size_t)written!=size){unlink(path);return 0;}
 unzFile archive=unzOpen64(path);unlink(path);if(!archive)return 0;
 unz_global_info64 global;unz_file_info64 info;char name[256]={0};
 int ok=0;
 if(unzGetGlobalInfo64(archive,&global)==UNZ_OK&&global.number_entry>0&&
    unzGoToFirstFile(archive)==UNZ_OK&&
    unzGetCurrentFileInfo64(archive,&info,name,sizeof(name),NULL,0,NULL,0)==UNZ_OK&&
    info.uncompressed_size<=sizeof(result->content)&&unzOpenCurrentFile(archive)==UNZ_OK){
  int got=unzReadCurrentFile(archive,result->content,sizeof(result->content));
  int close_status=unzCloseCurrentFile(archive);
  if(got>=0&&(unsigned long long)got==info.uncompressed_size&&close_status==UNZ_OK){
   result->entries=global.number_entry;result->name_len=strlen(name);
   result->content_len=got;memcpy(result->name,name,result->name_len);ok=1;
  }
 }
 unzClose(archive);return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_zip_result r;(void)parsarium_parse_zip(data,size,&r);return 0;}
