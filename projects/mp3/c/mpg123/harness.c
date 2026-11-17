#include "harness.h"
#include <mpg123.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 char path[]="/tmp/parsarium-mp3-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t offset=0;while(offset<size){ssize_t n=write(fd,data+offset,size-offset);if(n<=0){close(fd);unlink(path);return 0;}offset+=(size_t)n;}close(fd);
 if(mpg123_init()!=MPG123_OK){unlink(path);return 0;}
 int error=0;mpg123_handle *handle=mpg123_new(NULL,&error);
 if(!handle){unlink(path);mpg123_exit();return 0;}
 int ok=mpg123_open(handle,path)==MPG123_OK;unlink(path);
 if(ok)ok=mpg123_scan(handle)==MPG123_OK;
 mpg123_id3v1 *v1=NULL;mpg123_id3v2 *v2=NULL;
 if(ok)ok=mpg123_id3(handle,&v1,&v2)==MPG123_OK&&v2&&v2->title;
 if(ok){size_t n=v2->title->fill;while(n&&v2->title->p[n-1]==0)n--;ok=n<sizeof(result->title);if(ok){memcpy(result->title,v2->title->p,n);result->title[n]=0;result->id3v2_version=v2->version;}}
 mpg123_close(handle);mpg123_delete(handle);mpg123_exit();return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_mp3_result r;(void)parsarium_parse_mp3(data,size,&r);return 0;}
