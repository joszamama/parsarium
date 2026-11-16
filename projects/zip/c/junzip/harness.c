#include "harness.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <zlib.h>
#include <junzip.h>
static struct parsarium_zip_result *current;
static int parsed;
static int read_entry(FILE *archive,int index,JZFileHeader *central,char *name) {
 if(index!=0||!current)return 0;
 size_t name_len=strnlen(name,sizeof(current->name));
 if(!name_len||name_len>=sizeof(current->name))return 0;
 memcpy(current->name,name,name_len);current->name_len=name_len;
 if(central->uncompressedSize>sizeof(current->content))return 0;
 if(fseek(archive,central->offset,SEEK_SET))return 0;
 JZFileHeader local;char local_name[256];
 if(jzReadLocalFileHeader(archive,&local,local_name,sizeof(local_name))!=Z_OK ||
    strcmp(current->name,local_name) || local.uncompressedSize>sizeof(current->content))return 0;
 if(jzReadData(archive,&local,current->content)!=Z_OK)return 0;
 current->content_len=local.uncompressedSize;parsed=1;
 return 0;
}
int parsarium_parse_zip(const uint8_t *data,size_t size,struct parsarium_zip_result *result) {
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 char path[]="/tmp/parsarium-junzip-XXXXXX";
 int fd=mkstemp(path);if(fd<0)return 0;
 size_t written=0;
 while(written<size){ssize_t n=write(fd,data+written,size-written);if(n<=0){close(fd);unlink(path);return 0;}written+=(size_t)n;}
 FILE *archive=fdopen(fd,"rb");if(!archive){close(fd);unlink(path);return 0;}
 current=result;parsed=0;JZEndRecord end={0};
 int status=jzReadEndRecord(archive,&end);
 if(status==Z_OK)status=jzReadCentralDirectory(archive,&end,read_entry);
 fclose(archive);unlink(path);current=NULL;
 result->entries=end.numEntries;
 return status==Z_OK && parsed && result->entries>0;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_zip_result result;(void)parsarium_parse_zip(data,size,&result);return 0;
}
